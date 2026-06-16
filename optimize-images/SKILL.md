---
name: optimize-images
description: Design responsive image pipeline with srcset, modern formats, and lazy loading. Framework-specific implementations.
argument-hint: "[--framework next|nuxt|blazor|vanilla] [--format webp|avif|both]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Optimize Images Command

Design a responsive image optimization pipeline for web delivery.

## Usage

```bash
/cms:optimize-images --framework blazor
/cms:optimize-images --framework next --format avif
/cms:optimize-images --framework vanilla --format both
```

## Framework Options

- **next**: Next.js Image component
- **nuxt**: Nuxt Image module
- **blazor**: Blazor component with srcset
- **vanilla**: Plain HTML/CSS implementation

## Workflow

### Step 1: Parse Arguments

Extract framework and format preferences from command.

### Step 2: Invoke Skills

Invoke relevant skills:

- `image-optimization` - Responsive patterns
- `cdn-media-delivery` - CDN integration

### Step 3: Design Responsive Strategy

**Breakpoint Configuration:**

```yaml
responsive:
  breakpoints:
    mobile: 320
    mobile_lg: 480
    tablet: 768
    desktop: 1024
    desktop_lg: 1280
    wide: 1920

  device_pixel_ratios: [1, 2, 3]

  sizes_presets:
    thumbnail:
      default: 150px

    card:
      mobile: 100vw
      tablet: 50vw
      desktop: 33vw

    hero:
      default: 100vw

    content:
      mobile: 100vw
      tablet: 80vw
      desktop: 800px

  formats:
    priority: [avif, webp, jpg]
    fallback: jpg
```

### Step 4: Generate Implementation

**Blazor Component:**

```csharp
@* ResponsiveImage.razor *@
<picture>
    @foreach (var format in Formats)
    {
        <source type="@GetMimeType(format)"
                srcset="@GenerateSrcset(format)"
                sizes="@Sizes" />
    }
    <img src="@FallbackSrc"
         alt="@Alt"
         loading="@(Lazy ? "lazy" : "eager")"
         decoding="async"
         width="@Width"
         height="@Height"
         class="@CssClass"
         @attributes="AdditionalAttributes" />
</picture>

@code {
    [Parameter] public string Src { get; set; }
    [Parameter] public string Alt { get; set; }
    [Parameter] public int Width { get; set; }
    [Parameter] public int Height { get; set; }
    [Parameter] public string Sizes { get; set; } = "100vw";
    [Parameter] public bool Lazy { get; set; } = true;
    [Parameter] public string CssClass { get; set; }
    [Parameter] public string[] Formats { get; set; } = ["avif", "webp"];
    [Parameter(CaptureUnmatchedValues = true)]
    public Dictionary<string, object> AdditionalAttributes { get; set; }

    private int[] Widths => [320, 640, 768, 1024, 1280, 1920];

    private string FallbackSrc => GetTransformUrl(Src, Width, "jpg");

    private string GenerateSrcset(string format)
    {
        return string.Join(", ",
            Widths.Select(w => $"{GetTransformUrl(Src, w, format)} {w}w"));
    }

    private string GetTransformUrl(string src, int width, string format)
    {
        return $"/media/transform/{GetAssetId(src)}?w={width}&format={format}";
    }

    private string GetMimeType(string format) => format switch
    {
        "avif" => "image/avif",
        "webp" => "image/webp",
        "jpg" => "image/jpeg",
        _ => "image/jpeg"
    };
}
```

**Next.js Implementation:**

```tsx
// components/ResponsiveImage.tsx
import Image from 'next/image';

interface ResponsiveImageProps {
  src: string;
  alt: string;
  width: number;
  height: number;
  sizes?: string;
  priority?: boolean;
  className?: string;
}

export function ResponsiveImage({
  src,
  alt,
  width,
  height,
  sizes = '100vw',
  priority = false,
  className,
}: ResponsiveImageProps) {
  return (
    <Image
      src={src}
      alt={alt}
      width={width}
      height={height}
      sizes={sizes}
      priority={priority}
      className={className}
      placeholder="blur"
      blurDataURL={`/api/placeholder?w=10&h=${Math.round(10 * height / width)}`}
    />
  );
}

// next.config.js
module.exports = {
  images: {
    domains: ['cdn.example.com'],
    deviceSizes: [640, 768, 1024, 1280, 1920],
    imageSizes: [16, 32, 48, 64, 96, 128, 256, 384],
    formats: ['image/avif', 'image/webp'],
    minimumCacheTTL: 60 * 60 * 24 * 7, // 7 days
    loader: 'custom',
    loaderFile: './lib/imageLoader.ts',
  },
};

// lib/imageLoader.ts
export default function cmsImageLoader({
  src,
  width,
  quality,
}: {
  src: string;
  width: number;
  quality?: number;
}) {
  const q = quality || 85;
  return `${process.env.CDN_URL}/transform/${src}?w=${width}&q=${q}`;
}
```

**Vanilla HTML:**

```html
<!-- Responsive image with art direction -->
<picture>
  <!-- Art direction: different crop for mobile -->
  <source
    media="(max-width: 767px)"
    type="image/avif"
    srcset="
      /media/transform/hero-mobile?w=320&format=avif 320w,
      /media/transform/hero-mobile?w=640&format=avif 640w
    "
    sizes="100vw"
  />
  <source
    media="(max-width: 767px)"
    type="image/webp"
    srcset="
      /media/transform/hero-mobile?w=320&format=webp 320w,
      /media/transform/hero-mobile?w=640&format=webp 640w
    "
    sizes="100vw"
  />

  <!-- Desktop sources -->
  <source
    type="image/avif"
    srcset="
      /media/transform/hero?w=768&format=avif 768w,
      /media/transform/hero?w=1024&format=avif 1024w,
      /media/transform/hero?w=1920&format=avif 1920w
    "
    sizes="100vw"
  />
  <source
    type="image/webp"
    srcset="
      /media/transform/hero?w=768&format=webp 768w,
      /media/transform/hero?w=1024&format=webp 1024w,
      /media/transform/hero?w=1920&format=webp 1920w
    "
    sizes="100vw"
  />

  <!-- Fallback -->
  <img
    src="/media/transform/hero?w=1024&format=jpg"
    alt="Hero image description"
    loading="lazy"
    decoding="async"
    width="1920"
    height="1080"
  />
</picture>
```

### Step 5: Image Transform API

**Transform Service:**

```csharp
public class ImageTransformService
{
    public async Task<Stream> TransformAsync(
        Guid assetId,
        ImageTransformOptions options)
    {
        var asset = await _mediaRepository.GetAsync(assetId);
        var cacheKey = GenerateCacheKey(assetId, options);

        // Check cache first
        if (await _cache.ExistsAsync(cacheKey))
        {
            return await _cache.GetStreamAsync(cacheKey);
        }

        // Get original
        var original = await _storage.GetAsync(asset.StoragePath);

        // Transform using ImageSharp
        using var image = await Image.LoadAsync(original);

        // Apply focal point aware resize
        if (options.FocalPoint != null)
        {
            image.Mutate(x => x.Resize(new ResizeOptions
            {
                Size = new Size(options.Width, options.Height),
                Mode = ResizeMode.Crop,
                CenterCoordinates = new PointF(
                    options.FocalPoint.X * image.Width,
                    options.FocalPoint.Y * image.Height)
            }));
        }
        else
        {
            image.Mutate(x => x.Resize(options.Width, options.Height));
        }

        // Encode in requested format
        var output = new MemoryStream();
        await EncodeAsync(image, output, options.Format, options.Quality);

        // Cache result
        await _cache.SetAsync(cacheKey, output, TimeSpan.FromDays(7));

        output.Position = 0;
        return output;
    }
}

public record ImageTransformOptions
{
    public int Width { get; init; }
    public int? Height { get; init; }
    public string Format { get; init; } = "webp";
    public int Quality { get; init; } = 85;
    public string Fit { get; init; } = "contain";
    public FocalPoint FocalPoint { get; init; }
}
```

### Step 6: Performance Optimizations

**Loading Strategies:**

```yaml
loading:
  # Above the fold
  critical:
    loading: eager
    fetchpriority: high
    decoding: sync

  # Below the fold
  lazy:
    loading: lazy
    fetchpriority: auto
    decoding: async

  # Low priority
  deferred:
    loading: lazy
    fetchpriority: low
    decoding: async

  # Placeholder strategies
  placeholders:
    blur: true  # LQIP (Low Quality Image Placeholder)
    dominant_color: true
    skeleton: false
```

**Cache Configuration:**

```yaml
caching:
  # Browser cache
  browser:
    max_age: 31536000  # 1 year
    immutable: true
    stale_while_revalidate: 86400

  # CDN cache
  cdn:
    ttl: 604800  # 7 days
    vary: [Accept]  # Format negotiation

  # Transform cache
  transform:
    storage: redis
    ttl: 604800
    max_size: 10GB
    eviction: lru
```

## Metrics

Track image performance:

```yaml
metrics:
  - largest_contentful_paint
  - cumulative_layout_shift
  - time_to_first_byte
  - cache_hit_ratio
  - format_distribution
  - bandwidth_saved
```

## Related Skills

- `image-optimization` - Responsive patterns
- `cdn-media-delivery` - CDN configuration
- `media-asset-management` - Asset storage
