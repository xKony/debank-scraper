from browser_handler import DebankProfile
from config import MAX_THREADS, BATCH_SIZE, USE_NORDVPN, ADDRESSES_FILE
from nordvpn_utils import vpn_rotation
import asyncio
import reporter
import random
from logger import get_logger

# Initialize Logger
log = get_logger(__name__)

# Global semaphore to control concurrency
sem = asyncio.Semaphore(MAX_THREADS)


async def process_address(address: str, task_id: int):
    async with sem:
        log.info(f"[{task_id}] Processing: {address}")
        profile = DebankProfile(address)
        try:
            # Prevent hanging on browser start
            await asyncio.wait_for(profile.start_browser(), timeout=30)

            # Parsing logic
            await profile.parse_chains()
            await profile.parse_projects()
            # await profile.parse_tokens() # not working currently

            log.info(f"[{task_id}] Finished: {address}")

        except asyncio.TimeoutError:
            log.error(f"[{task_id}] Timeout error for {address} (Browser stuck)")
        except Exception as e:
            log.error(f"[{task_id}] Error processing {address}: {e}")
        finally:
            # Guaranteed cleanup
            try:
                await profile.close_browser()
            except Exception:
                pass


async def run_batch(batch_addresses):
    tasks = []
    for i, (addr, original_index) in enumerate(batch_addresses):
        # We pass the original task ID for logging
        tasks.append(process_address(addr, original_index))

        await asyncio.sleep(random.uniform(0.5, 1.5))

    # This waits until the entire batch is done.
    await asyncio.gather(*tasks)


async def main(addresses_map: dict):
    if not addresses_map:
        log.warning("No addresses to process.")
        return

    # Convert dict items to a list for slicing
    all_items = list(addresses_map.items())
    total_items = len(all_items)

    # Calculate number of batches
    rotation_limit = BATCH_SIZE if (USE_NORDVPN and BATCH_SIZE > 0) else total_items

    log.info(f"Starting processing. Total: {total_items}. Batch size: {rotation_limit}")

    # Initial VPN setup
    if USE_NORDVPN:
        log.info(">>> Initial VPN Setup...")
        try:
            if asyncio.iscoroutinefunction(vpn_rotation):
                await vpn_rotation()
            else:
                await asyncio.to_thread(vpn_rotation)
        except Exception as e:
            log.error(f"Initial VPN rotation failed: {e}")

    processed_count = 0

    # --- BATCH LOOP ---
    for i in range(0, total_items, rotation_limit):
        # Create the slice (the batch)
        batch = all_items[i : i + rotation_limit]

        log.info(
            f"--- Starting Batch {i // rotation_limit + 1} (Addresses {i+1} to {min(i + rotation_limit, total_items)} out of {total_items} total) ---"
        )

        # Run the batch and wait for ALL in this batch to finish
        await run_batch(batch)

        # Update and print counter
        processed_count += len(batch)
        log.info(
            f">>> Progress update: {processed_count}/{total_items} addresses processed."
        )

        # Check if we need to rotate (and if we are not at the very end)
        if USE_NORDVPN and (i + rotation_limit < total_items):
            log.info(">>> Batch complete. Rotating VPN...")
            try:
                await asyncio.sleep(2)  # Wait for sockets to clear

                if asyncio.iscoroutinefunction(vpn_rotation):
                    await vpn_rotation()
                else:
                    await asyncio.to_thread(vpn_rotation)

                log.info(">>> VPN Rotated. Waiting 5s for stability...")
                await asyncio.sleep(5)
            except Exception as e:
                log.error(f"VPN Rotation failed: {e}")

    log.info("Every task finished.")

    # --- MOVED: Finalize reporter ONLY HERE ---
    log.info("Saving final report...")
    try:
        await asyncio.to_thread(reporter.finalize_outputs)
        log.info("Report saved successfully.")
    except Exception as e:
        log.error(f"Error saving final report: {e}")


if __name__ == "__main__":
    # load addresses from file
    try:
        address_order_map = reporter.load_address_order(ADDRESSES_FILE)
        if not address_order_map:
            log.critical(f"Error: No addresses found in {ADDRESSES_FILE}.")
            exit(1)
    except FileNotFoundError:
        log.critical(f"Error: File ‘{ADDRESSES_FILE}’ not found.")
        exit(1)

    # pass address list to reporter
    reporter.init_reporter(address_order_map)

    # run main async loop
    try:
        asyncio.run(main(address_order_map))
    except KeyboardInterrupt:
        log.warning("Script interrupted by user.")
        exit(0)
