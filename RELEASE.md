# Open edX Course Test Release Notes

## New in 0.3.0
- Course image validation
  - It exists
  - It is an image
  - It is the correct image type (PNG or JPG)
  - It warns if the aspect ratio isn't correct (1.75)
- All image tags in content have `alt` attributes for accessibility
- All video units have `show_captions` set to true (warns only)
- Link checking
  - `/static/` magic links point at assets that exist in the course
  - `/jump_to/` links point at internally valid courseware
  - `/jump_to_id/` point at valid urls within the course
  - `http[s]` links are tested with HEAD and validated to return 200 status code
- Reorganized python test module

## New in 0.2.0
- First open source release
- Organized structure
- Licensed
