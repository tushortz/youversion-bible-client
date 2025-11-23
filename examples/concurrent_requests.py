#!/usr/bin/env python3
"""
Concurrent requests example for YouVersion Bible Client

This example demonstrates how to make concurrent API requests:
1. Using asyncio.gather() for parallel requests
2. Using asyncio.as_completed() for streaming results
3. Using asyncio.create_task() for background tasks
4. Error handling in concurrent operations
5. Rate limiting and batching

Make sure to set up your .env file with YOUVERSION_USERNAME and YOUVERSION_PASSWORD
"""

import asyncio
import os
import time

from youversion.clients import AsyncClient


async def fetch_single_data(
    client: AsyncClient, data_type: str, page: int = 1
) -> tuple:
    """Fetch a single type of data and return type and result"""
    try:
        if data_type == "votd":
            result = await client.verse_of_the_day()
        elif data_type == "moments":
            result = await client.moments(page=page)
        elif data_type == "highlights":
            result = await client.highlights(page=page)
        elif data_type == "notes":
            result = await client.notes(page=page)
        elif data_type == "bookmarks":
            result = await client.bookmarks(page=page)
        elif data_type == "my_images":
            result = await client.my_images(page=page)
        elif data_type == "plan_progress":
            result = await client.plan_progress(page=page)
        elif data_type == "plan_subscriptions":
            result = await client.plan_subscriptions(page=page)
        elif data_type == "plan_completions":
            result = await client.plan_completions(page=page)
        elif data_type == "badges":
            result = await client.badges(page=page)
        elif data_type == "convert_note_to_md":
            result = await client.convert_note_to_md()
        else:
            raise ValueError(f"Unknown data type: {data_type}")

        return data_type, result, None
    except Exception as e:
        return data_type, None, e


async def demonstrate_gather_pattern():
    """Demonstrate using asyncio.gather() for parallel requests"""
    print("🔄 Demonstrating asyncio.gather() pattern...")

    try:
        async with AsyncClient() as client:
            start_time = time.time()

            # Make multiple requests in parallel
            results = await asyncio.gather(
                fetch_single_data(client, "votd"),
                fetch_single_data(client, "moments", 1),
                fetch_single_data(client, "highlights", 1),
                fetch_single_data(client, "notes", 1),
                fetch_single_data(client, "bookmarks", 1),
                fetch_single_data(client, "my_images", 1),
                fetch_single_data(client, "plan_progress", 1),
                fetch_single_data(client, "plan_subscriptions", 1),
                fetch_single_data(client, "plan_completions", 1),
                fetch_single_data(client, "badges", 1),
                fetch_single_data(client, "convert_note_to_md"),
                return_exceptions=True,
            )

            end_time = time.time()
            duration = end_time - start_time

            print(f"   ⏱️  Completed {len(results)} requests in {duration:.2f} seconds")

            # Process results
            for data_type, result, error in results:
                if error:
                    print(f"   ❌ {data_type}: Error - {error}")
                else:
                    if data_type == "votd":
                        print(f"   📖 {data_type}: Day {result.day}")
                    else:
                        print(f"   📋 {data_type}: {len(result)} items")

    except Exception as e:
        print(f"   ❌ Error in gather pattern: {e}")


async def demonstrate_as_completed_pattern():
    """Demonstrate using asyncio.as_completed() for streaming results"""
    print("\n🌊 Demonstrating asyncio.as_completed() pattern...")

    try:
        async with AsyncClient() as client:
            start_time = time.time()

            # Create tasks for different requests
            tasks = [
                asyncio.create_task(fetch_single_data(client, "votd")),
                asyncio.create_task(fetch_single_data(client, "moments", 1)),
                asyncio.create_task(fetch_single_data(client, "highlights", 1)),
                asyncio.create_task(fetch_single_data(client, "notes", 1)),
                asyncio.create_task(fetch_single_data(client, "bookmarks", 1)),
                asyncio.create_task(fetch_single_data(client, "my_images", 1)),
                asyncio.create_task(fetch_single_data(client, "plan_progress", 1)),
                asyncio.create_task(fetch_single_data(client, "plan_subscriptions", 1)),
                asyncio.create_task(fetch_single_data(client, "plan_completions", 1)),
                asyncio.create_task(fetch_single_data(client, "badges", 1)),
                asyncio.create_task(fetch_single_data(client, "convert_note_to_md")),
            ]

            # Process results as they complete
            completed_count = 0
            for task in asyncio.as_completed(tasks):
                data_type, result, error = await task
                completed_count += 1

                elapsed = time.time() - start_time

                if error:
                    print(
                        f"   ❌ {data_type} (completed {completed_count}/{len(tasks)} in {elapsed:.2f}s): Error"
                    )
                else:
                    if data_type == "votd":
                        print(
                            f"   📖 {data_type} (completed {completed_count}/{len(tasks)} in {elapsed:.2f}s): Day {result.day}"
                        )
                    else:
                        print(
                            f"   📋 {data_type} (completed {completed_count}/{len(tasks)} in {elapsed:.2f}s): {len(result)} items"
                        )

    except Exception as e:
        print(f"   ❌ Error in as_completed pattern: {e}")


async def demonstrate_batch_requests():
    """Demonstrate batching requests with rate limiting"""
    print("\n📦 Demonstrating batch requests with rate limiting...")

    try:
        async with AsyncClient() as client:
            # Request multiple pages of moments
            pages = [1, 2, 3, 4, 5]
            batch_size = 2  # Process 2 requests at a time

            all_moments = []

            for i in range(0, len(pages), batch_size):
                batch = pages[i : i + batch_size]
                print(f"   📄 Processing batch: pages {batch}")

                # Create tasks for this batch
                tasks = [
                    asyncio.create_task(fetch_single_data(client, "moments", page))
                    for page in batch
                ]

                # Wait for batch to complete
                batch_results = await asyncio.gather(*tasks, return_exceptions=True)

                # Process batch results
                for page, batch_result in zip(batch, batch_results):
                    _data_type, result, error = batch_result
                    if error:
                        print(f"      ❌ Page {page}: Error - {error}")
                    else:
                        print(f"      ✅ Page {page}: {len(result)} moments")
                        all_moments.extend(result)

                # Rate limiting: wait between batches
                if i + batch_size < len(pages):
                    print("      ⏸️  Waiting 1 second before next batch...")
                    await asyncio.sleep(1)

            print(f"   📊 Total moments collected: {len(all_moments)}")

    except Exception as e:
        print(f"   ❌ Error in batch requests: {e}")


async def demonstrate_background_tasks():
    """Demonstrate background tasks"""
    print("\n🔄 Demonstrating background tasks...")

    async def background_fetcher(client: AsyncClient, data_type: str, interval: float):
        """Background task that fetches data periodically"""
        try:
            while True:
                data_type, result, error = await fetch_single_data(client, data_type)

                if error:
                    print(f"   🔄 Background {data_type}: Error - {error}")
                else:
                    if data_type == "votd":
                        print(f"   🔄 Background {data_type}: Day {result.day}")
                    else:
                        print(f"   🔄 Background {data_type}: {len(result)} items")

                await asyncio.sleep(interval)
        except asyncio.CancelledError:
            print(f"   🛑 Background {data_type} task cancelled")
        except Exception as e:
            print(f"   ❌ Background {data_type} error: {e}")

    try:
        async with AsyncClient() as client:
            # Start background tasks
            tasks = [
                asyncio.create_task(background_fetcher(client, "votd", 2.0)),
                asyncio.create_task(background_fetcher(client, "moments", 3.0)),
            ]

            print("   🚀 Background tasks started")

            # Let them run for a bit
            await asyncio.sleep(8)

            # Cancel background tasks
            for task in tasks:
                task.cancel()

            # Wait for cancellation to complete
            await asyncio.gather(*tasks, return_exceptions=True)

            print("   🛑 Background tasks stopped")

    except Exception as e:
        print(f"   ❌ Error in background tasks: {e}")


async def demonstrate_error_handling_in_concurrent():
    """Demonstrate error handling in concurrent operations"""
    print("\n⚠️  Demonstrating error handling in concurrent operations...")

    async def fetch_with_retry(
        client: AsyncClient, data_type: str, max_retries: int = 3
    ):
        """Fetch data with retry logic"""
        for attempt in range(max_retries):
            try:
                data_type, result, error = await fetch_single_data(client, data_type)
                if error:
                    raise error
                return result
            except Exception as e:
                if attempt < max_retries - 1:
                    print(
                        f"   ⚠️  {data_type} attempt {attempt + 1} failed, retrying..."
                    )
                    await asyncio.sleep(1)
                else:
                    print(f"   ❌ {data_type} failed after {max_retries} attempts: {e}")
                    raise

    try:
        async with AsyncClient() as client:
            # Try to fetch data with retry logic
            tasks = [
                asyncio.create_task(fetch_with_retry(client, "votd")),
                asyncio.create_task(fetch_with_retry(client, "moments")),
                asyncio.create_task(fetch_with_retry(client, "highlights")),
                asyncio.create_task(fetch_with_retry(client, "notes")),
                asyncio.create_task(fetch_with_retry(client, "bookmarks")),
                asyncio.create_task(fetch_with_retry(client, "my_images")),
                asyncio.create_task(fetch_with_retry(client, "plan_progress")),
                asyncio.create_task(fetch_with_retry(client, "plan_subscriptions")),
                asyncio.create_task(fetch_with_retry(client, "plan_completions")),
                asyncio.create_task(fetch_with_retry(client, "badges")),
                asyncio.create_task(fetch_with_retry(client, "convert_note_to_md")),
            ]

            results = await asyncio.gather(*tasks, return_exceptions=True)

            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"   ❌ Task {i + 1} failed: {result}")
                else:
                    print(f"   ✅ Task {i + 1} succeeded")

    except Exception as e:
        print(f"   ❌ Error in concurrent error handling: {e}")


async def main():
    """Main function demonstrating concurrent patterns"""

    # Check if credentials are available
    username = os.getenv("YOUVERSION_USERNAME")
    password = os.getenv("YOUVERSION_PASSWORD")

    if not username or not password:
        print(
            "❌ Error: Please set YOUVERSION_USERNAME and YOUVERSION_PASSWORD environment variables"
        )
        print("   Or create a .env file with your credentials")
        return

    print("🚀 Starting YouVersion Bible Client Concurrent Requests Example")
    print("=" * 75)

    # Run all demonstrations
    await demonstrate_gather_pattern()
    await demonstrate_as_completed_pattern()
    await demonstrate_batch_requests()
    await demonstrate_background_tasks()
    await demonstrate_error_handling_in_concurrent()

    print("\n✅ Concurrent requests example completed!")


if __name__ == "__main__":
    # Run the async main function
    asyncio.run(main())
