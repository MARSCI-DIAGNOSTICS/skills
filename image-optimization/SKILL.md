---
name: image-optimization
description: Use when implementing responsive images, format conversion, focal point cropping, or image processing pipelines. Covers srcset generation, WebP/AVIF conversion, lazy loading, and image transformation APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Image Optimization

Guidance for implementing responsive images, format optimization, and image processing pipelines for headless CMS.

## When to Use This Skill

- Implementing responsive image delivery
- Converting images to modern formats (WebP, AVIF)
- Building image processing pipelines
- Implementing focal point cropping
- Optimizing image loading performance

## Responsive Image Patterns

### Srcset for Resolution Switching

```html
<!-- Basic srcset with width descriptors -->
<img
  src="/images/hero.jpg"
  srcset="
    /images/hero-400w.jpg 400w,
    /images/hero-800w.jpg 800w,
    /images/hero-1200w.jpg 1200w,
    /images/hero-1600w.jpg 1600w
  "
  sizes="(max-width: 600px) 100vw, (max-width: 1200px) 50vw, 800px"
  alt="Hero image"
>

<!-- Srcset with pixel density -->
<img
  src="/images/logo.png"
  srcset="
    /images/logo.png 1x,
    /images/logo@2x.png 2x,
    /images/logo@3x.png 3x
  "
  alt="Logo"
>
```

### Picture Element for Art Direction

```html
<picture>
  <!-- Mobile: Square crop -->
  <source
    media="(max-width: 600px)"
    srcset="/images/hero-mobile.webp"
    type="image/webp"
  >
  <source
    media="(max-width: 600px)"
    srcset="/images/hero-mobile.jpg"
  >

  <!-- Desktop: Wide crop -->
  <source
    srcset="/images/hero-desktop.webp"
    type="image/webp"
  >

  <!-- Fallback -->
  <img src="/images/hero-desktop.jpg" alt="Hero">
</picture>
```

## Image Processing Service

### Core Processing

```csharp
public class ImageProcessingService
{
    public async Task<Stream> ProcessAsync(
        Stream source,
        ImageProcessingOptions options)
    {
        using var image = await Image.LoadAsync(source);

        // Resize
        if (options.Width.HasValue || options.Height.HasValue)
        {
            var resizeOptions = new ResizeOptions
            {
                Size = new Size(
                    options.Width ?? 0,
                    options.Height ?? 0),
                Mode = options.ResizeMode,
                Position = options.FocalPoint != null
                    ? CalculateAnchor(options.FocalPoint, image.Size)
                    : AnchorPositionMode.Center
            };

            image.Mutate(x => x.Resize(resizeOptions));
        }

        // Apply effects
        if (options.Blur > 0)
        {
            image.Mutate(x => x.GaussianBlur(options.Blur));
        }

        if (options.Grayscale)
        {
            image.Mutate(x => x.Grayscale());
        }

        // Encode to target format
        var outputStream = new MemoryStream();
        await EncodeAsync(image, outputStream, options);

        outputStream.Position = 0;
        return outputStream;
    }

    private async Task EncodeAsync(
        Image image,
        Stream output,
        ImageProcessingOptions options)
    {
        switch (options.Format)
        {
            case ImageFormat.WebP:
                await image.SaveAsWebpAsync(output, new WebpEncoder
                {
                    Quality = options.Quality,
                    Method = WebpEncodingMethod.BestQuality
                });
                break;

            case ImageFormat.Avif:
                await image.SaveAsAvifAsync(output, new AvifEncoder
                {
                    Quality = options.Quality
                });
                break;

            case ImageFormat.Jpeg:
                await image.SaveAsJpegAsync(output, new JpegEncoder
                {
                    Quality = options.Quality,
                    ColorType = JpegEncodingColor.YCbCrRatio420
                });
                break;

            case ImageFormat.Png:
                await image.SaveAsPngAsync(output, new PngEncoder
                {
                    CompressionLevel = PngCompressionLevel.BestCompression
                });
                break;
        }
    }
}

public class ImageProcessingOptions
{
    public int? Width { get; set; }
    public int? Height { get; set; }
    public ResizeMode ResizeMode { get; set; } = ResizeMode.Max;
    public FocalPoint? FocalPoint { get; set; }
    public ImageFormat Format { get; set; } = ImageFormat.WebP;
    public int Quality { get; set; } = 80;
    public float Blur { get; set; }
    public bool Grayscale { get; set; }
}

public class FocalPoint
{
    public float X { get; set; } // 0-1, left to right
    public float Y { get; set; } // 0-1, top to bottom
}

public enum ImageFormat
{
    Jpeg,
    Png,
    WebP,
    Avif,
    Gif
}
```

### Preset-Based Processing

```csharp
public class ImagePresets
{
    public static readonly Dictionary<string, ImageProcessingOptions> Presets = new()
    {
        ["thumbnail"] = new()
        {
            Width = 150,
            Height = 150,
            ResizeMode = ResizeMode.Crop,
            Format = ImageFormat.WebP,
            Quality = 75
        },
        ["card"] = new()
        {
            Width = 400,
            Height = 300,
            ResizeMode = ResizeMode.Crop,
            Format = ImageFormat.WebP,
            Quality = 80
        },
        ["hero"] = new()
        {
            Width = 1920,
            Height = 800,
            ResizeMode = ResizeMode.Crop,
            Format = ImageFormat.WebP,
            Quality = 85
        },
        ["og-image"] = new()
        {
            Width = 1200,
            Height = 630,
            ResizeMode = ResizeMode.Crop,
            Format = ImageFormat.Jpeg,
            Quality = 90
        },
        ["blur-placeholder"] = new()
        {
            Width = 20,
            Height = 20,
            Format = ImageFormat.Jpeg,
            Quality = 30,
            Blur = 5
        }
    };
}
```

## Focal Point Cropping

### Focal Point Model

```csharp
public class FocalPointService
{
    public AnchorPositionMode CalculateAnchor(
        FocalPoint focal,
        Size imageSize,
        Size targetSize)
    {
        // Calculate which part of image will be cropped
        var imageAspect = (float)imageSize.Width / imageSize.Height;
        var targetAspect = (float)targetSize.Width / targetSize.Height;

        if (Math.Abs(imageAspect - targetAspect) < 0.01f)
        {
            return AnchorPositionMode.Center;
        }

        // Determine crop direction
        var cropHorizontal = imageAspect > targetAspect;

        if (cropHorizontal)
        {
            // Cropping sides, use X focal point
            return focal.X switch
            {
                < 0.33f => AnchorPositionMode.Left,
                > 0.66f => AnchorPositionMode.Right,
                _ => AnchorPositionMode.Center
            };
        }
        else
        {
            // Cropping top/bottom, use Y focal point
            return focal.Y switch
            {
                < 0.33f => AnchorPositionMode.Top,
                > 0.66f => AnchorPositionMode.Bottom,
                _ => AnchorPositionMode.Center
            };
        }
    }
}
```

### Storing Focal Point

```csharp
public class MediaItem
{
    public Guid Id { get; set; }
    public string FileName { get; set; } = string.Empty;

    // Focal point for smart cropping
    public FocalPoint? FocalPoint { get; set; }
}

// Set via API
PATCH /api/media/{id}
{
  "focalPoint": { "x": 0.3, "y": 0.2 }
}
```

## On-the-Fly Image Transformation

### URL-Based Transformation

```text
# Base URL
https://cdn.example.com/media/hero.jpg

# With transformations
https://cdn.example.com/media/hero.jpg?w=800&h=600&fit=crop
https://cdn.example.com/media/hero.jpg?w=400&format=webp&q=80
https://cdn.example.com/media/hero.jpg?preset=thumbnail
```

### Transformation Endpoint

```csharp
[Route("media/{*path}")]
public class ImageTransformController : ControllerBase
{
    [HttpGet]
    [ResponseCache(Duration = 31536000, VaryByQueryKeys = new[] { "*" })]
    public async Task<IActionResult> GetTransformed(
        string path,
        [FromQuery] int? w,
        [FromQuery] int? h,
        [FromQuery] string? format,
        [FromQuery] int? q,
        [FromQuery] string? fit,
        [FromQuery] string? preset)
    {
        // Get original image
        var original = await _mediaService.GetStreamAsync(path);
        if (original == null) return NotFound();

        // Build options from query or preset
        var options = preset != null
            ? ImagePresets.Presets.GetValueOrDefault(preset) ?? new()
            : new ImageProcessingOptions
            {
                Width = w,
                Height = h,
                Format = ParseFormat(format),
                Quality = q ?? 80,
                ResizeMode = ParseFit(fit)
            };

        // Process image
        var processed = await _imageProcessor.ProcessAsync(original, options);

        return File(processed, GetMimeType(options.Format));
    }
}
```

## Srcset Generation

### Responsive Image Service

```csharp
public class ResponsiveImageService
{
    private readonly int[] _defaultWidths = { 320, 640, 960, 1280, 1920 };

    public ResponsiveImageData GenerateSrcset(
        MediaItem media,
        ResponsiveImageOptions? options = null)
    {
        options ??= new ResponsiveImageOptions();
        var widths = options.Widths ?? _defaultWidths;

        var srcset = widths
            .Where(w => w <= (media.Metadata.Width ?? int.MaxValue))
            .Select(w => new SrcsetEntry
            {
                Url = BuildTransformUrl(media, w, options.Format),
                Width = w
            })
            .ToList();

        return new ResponsiveImageData
        {
            Src = BuildTransformUrl(media, options.DefaultWidth, options.Format),
            Srcset = srcset,
            Sizes = options.Sizes ?? "(max-width: 1200px) 100vw, 1200px",
            Alt = media.Metadata.Alt ?? "",
            Width = media.Metadata.Width,
            Height = media.Metadata.Height,
            BlurDataUrl = options.IncludeBlurPlaceholder
                ? BuildTransformUrl(media, 20, ImageFormat.Jpeg, blur: 5)
                : null
        };
    }

    private string BuildTransformUrl(
        MediaItem media,
        int width,
        ImageFormat format,
        int? blur = null)
    {
        var query = $"?w={width}&format={format.ToString().ToLower()}";
        if (blur.HasValue) query += $"&blur={blur}";
        return $"{_cdnBaseUrl}/media/{media.StoragePath}{query}";
    }
}

public class ResponsiveImageData
{
    public string Src { get; set; } = string.Empty;
    public List<SrcsetEntry> Srcset { get; set; } = new();
    public string Sizes { get; set; } = string.Empty;
    public string Alt { get; set; } = string.Empty;
    public int? Width { get; set; }
    public int? Height { get; set; }
    public string? BlurDataUrl { get; set; }
}

public class SrcsetEntry
{
    public string Url { get; set; } = string.Empty;
    public int Width { get; set; }

    public override string ToString() => $"{Url} {Width}w";
}
```

## Low-Quality Image Placeholders (LQIP)

### Blur Hash Generation

```csharp
public class BlurHashService
{
    public string GenerateBlurHash(Image image, int componentsX = 4, int componentsY = 3)
    {
        // Resize to small dimensions for hash calculation
        using var small = image.Clone(x => x.Resize(32, 32));

        // Calculate blur hash
        var pixels = new Pixel[32, 32];
        for (var y = 0; y < 32; y++)
        {
            for (var x = 0; x < 32; x++)
            {
                var pixel = small[x, y];
                pixels[x, y] = new Pixel(pixel.R, pixel.G, pixel.B);
            }
        }

        return BlurHash.Encode(pixels, componentsX, componentsY);
    }
}
```

### Placeholder Strategies

| Strategy | Size | Quality | Use Case |
| -------- | ---- | ------- | -------- |
| Blur hash | ~30 chars | Good | Inline in HTML |
| Tiny JPEG | ~500 bytes | Medium | Data URL |
| Dominant color | 7 chars | Simple | CSS background |
| SVG trace | ~2KB | Good | Artistic sites |

## Performance Best Practices

### Lazy Loading

```html
<!-- Native lazy loading -->
<img
  src="/images/photo.jpg"
  loading="lazy"
  decoding="async"
  alt="Photo"
>

<!-- With blur placeholder -->
<div class="image-container" style="background: url(data:image/jpeg;base64,...)">
  <img
    src="/images/photo.jpg"
    loading="lazy"
    onload="this.parentElement.style.background = 'none'"
    alt="Photo"
  >
</div>
```

### Format Selection

```csharp
public ImageFormat SelectOptimalFormat(string acceptHeader, ImageFormat preferred)
{
    if (acceptHeader.Contains("image/avif"))
        return ImageFormat.Avif;

    if (acceptHeader.Contains("image/webp"))
        return ImageFormat.WebP;

    return preferred;
}
```

## Image API Response

```json
{
  "data": {
    "id": "media-123",
    "original": {
      "url": "https://cdn.example.com/media/original/hero.jpg",
      "width": 3840,
      "height": 2160,
      "mimeType": "image/jpeg",
      "sizeBytes": 2456789
    },
    "responsive": {
      "src": "https://cdn.example.com/media/hero.jpg?w=1280&format=webp",
      "srcset": "https://cdn.example.com/media/hero.jpg?w=320&format=webp 320w, ...",
      "sizes": "(max-width: 1200px) 100vw, 1200px"
    },
    "placeholder": {
      "blurHash": "LEHV6nWB2yk8pyo0adR*.7kCMdnj",
      "dataUrl": "data:image/jpeg;base64,/9j/4AAQ..."
    },
    "focalPoint": { "x": 0.5, "y": 0.3 }
  }
}
```

## Related Skills

- `media-asset-management` - Media library and upload
- `cdn-media-delivery` - CDN integration and caching
- `headless-api-design` - Image API endpoints
