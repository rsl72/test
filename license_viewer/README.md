# License Viewer Sample

This sample demonstrates a Qt widget that reads a Markdown file containing
multiple licenses. Each license title appears with a "Show license" button
and the full text expands in an accordion style. Nested headings in the
Markdown file create nested accordions.

The sample also includes an MFC application entry point showing how the
widget can be hosted in a Windows application built with CMake.

## Build (Windows)

```
cmake -S . -B build -G "Visual Studio 17 2022" -A x64
cmake --build build
```

Make sure Qt 5 and Visual Studio MFC components are installed.
