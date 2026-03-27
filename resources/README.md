# Resources Directory

This directory contains application resources such as icons, images, and other assets.

## Structure

```
resources/
├── icons/          # Application icons
├── images/         # UI images and graphics
└── styles/         # Custom stylesheets
```

## Adding Resources

Place resource files here and reference them in the Qt application using Qt's resource system or direct file paths.

### Icons

Add application icons in various sizes:
- 16x16, 24x24, 32x32, 48x48, 64x64, 128x128, 256x256

### Images

Add UI images, logos, splash screens, etc.

### Styles

Add custom Qt stylesheets (.qss files) for theming.

## Qt Resource Files

To use Qt's resource system, create a `.qrc` file:

```xml
<RCC>
    <qresource prefix="/icons">
        <file>icons/app-icon.png</file>
    </qresource>
</RCC>
```

Then add to CMakeLists.txt:
```cmake
qt_add_resources(RESOURCES resources.qrc)
```
