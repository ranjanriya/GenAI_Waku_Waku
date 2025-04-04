import os
import shutil

def process_images(
    source_folder,
    destination_folder,
    chapter_filter,
    page_filter,
    mode='select'  # or 'select' or 'exclude'
):
    os.makedirs(destination_folder, exist_ok=True)

    # Convert range to list if needed
    if isinstance(chapter_filter, range):
        chapter_filter = list(chapter_filter)
    if isinstance(page_filter, range):
        page_filter = list(page_filter)

    for filename in os.listdir(source_folder):
        if filename.endswith('.png') and len(filename) == 10:
            chapter = int(filename[:3])
            page = int(filename[3:6])

            chapter_match = (
                chapter_filter == 'all' or
                (isinstance(chapter_filter, list) and chapter in chapter_filter)
            )

            page_match = (
                page_filter == 'all' or
                (isinstance(page_filter, list) and page in page_filter)
            )

            # Determine if file should be copied
            if (mode == 'select' and chapter_match and page_match) or \
               (mode == 'exclude' and not (chapter_match and page_match)):
                src = os.path.join(source_folder, filename)
                dst = os.path.join(destination_folder, filename)
                shutil.copy2(src, dst)

    print(f"{mode.capitalize()}ion complete. Images copied to '{destination_folder}'.")


def select(
    source_folder='sorted',
    destination_folder='selected',
    selected_chapters='all',
    selected_pages='all'
):
    process_images(
        source_folder,
        destination_folder,
        chapter_filter=selected_chapters,
        page_filter=selected_pages,
        mode='select'
    )


def exclude(
    source_folder='downloaded_images',
    destination_folder='sorted',
    exclude_from_chapters='all',
    pages_to_exclude='all'
):
    process_images(
        source_folder,
        destination_folder,
        chapter_filter=exclude_from_chapters,
        page_filter=pages_to_exclude,
        mode='exclude'
    )

# Example usage:
select(selected_chapters=[5], selected_pages='all')
#exclude(exclude_from_chapters='all', pages_to_exclude=[1])
