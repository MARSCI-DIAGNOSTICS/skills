---
name: design-media-strategy
description: Design media and DAM architecture including storage, processing, and delivery. Covers images, video, and documents.
argument-hint: "[--scope images|video|documents|all] [--storage azure|aws|local]"
allowed-tools: Read, Glob, Grep, Task, Skill, AskUserQuestion
---

# Design Media Strategy Command

Design a comprehensive media and Digital Asset Management (DAM) architecture.

## Usage

```bash
/cms:design-media-strategy --scope all
/cms:design-media-strategy --scope images --storage azure
/cms:design-media-strategy --scope video --storage aws
```

## Scope Options

- **images**: Image storage, optimization, delivery
- **video**: Video hosting, transcoding, streaming
- **documents**: PDF, Office documents, downloads
- **all**: Complete media strategy

## Workflow

### Step 1: Parse Arguments

Extract scope and storage provider from command.

### Step 2: Gather Requirements

Use AskUserQuestion to understand:

- What is the expected media volume?
- Are there specific format requirements?
- What CDN/delivery requirements exist?
- Are there compliance/security needs (watermarking, access control)?

### Step 3: Invoke Agent

Invoke `cms-advisor media-strategy` agent for comprehensive analysis.

### Step 4: Generate Storage Architecture

**Azure Blob Storage Configuration:**

```yaml
storage:
  provider: azure_blob

  containers:
    - name: cms-media-originals
      access: private
      purpose: Original uploaded files
      retention: indefinite

    - name: cms-media-processed
      access: private
      purpose: Processed/transformed files
      retention: 30_days_unused

    - name: cms-media-public
      access: blob  # Public read, private list
      purpose: Public CDN-served assets
      cdn: true

  lifecycle_rules:
    - name: archive-old-originals
      condition:
        days_since_modification: 365
      action: move_to_cool

    - name: delete-temp
      prefix: temp/
      condition:
        days_since_creation: 7
      action: delete

  security:
    encryption: AES256
    https_only: true
    sas_tokens:
      enabled: true
      max_duration: 1_hour
```

**AWS S3 Configuration:**

```yaml
storage:
  provider: aws_s3

  buckets:
    - name: cms-media-originals
      region: us-east-1
      versioning: true

    - name: cms-media-processed
      region: us-east-1
      intelligent_tiering: true

  cloudfront:
    enabled: true
    price_class: PriceClass_100
    origins:
      - bucket: cms-media-processed
        path: /public/*
    behaviors:
      - path: /images/*
        compress: true
        cache_ttl: 86400
      - path: /videos/*
        streaming: true
```

### Step 5: Design Processing Pipeline

**Image Processing:**

```yaml
image_pipeline:
  upload:
    max_size: 50MB
    allowed_types: [jpg, jpeg, png, gif, webp, svg, avif]
    scan_for_malware: true
    extract_metadata: true

  processing:
    profiles:
      thumbnail:
        width: 150
        height: 150
        fit: cover
        format: webp
        quality: 80

      small:
        width: 400
        height: 300
        fit: contain
        format: webp
        quality: 85

      medium:
        width: 800
        height: 600
        fit: contain
        format: webp
        quality: 85

      large:
        width: 1600
        height: 1200
        fit: contain
        format: webp
        quality: 90

      hero:
        width: 1920
        height: 1080
        fit: cover
        format: webp
        quality: 90
        focal_point: true

    responsive_breakpoints:
      - 320
      - 640
      - 768
      - 1024
      - 1280
      - 1920

    formats:
      modern: [avif, webp]
      fallback: jpg

  optimization:
    strip_metadata: true
    progressive: true
    preserve_color_profile: sRGB
```

**Video Processing:**

```yaml
video_pipeline:
  upload:
    max_size: 5GB
    allowed_types: [mp4, mov, avi, webm, mkv]

  transcoding:
    provider: azure_media_services  # or aws_mediaconvert

    profiles:
      web_hd:
        codec: h264
        resolution: 1080p
        bitrate: 5000kbps
        audio: aac_128

      web_sd:
        codec: h264
        resolution: 720p
        bitrate: 2500kbps
        audio: aac_128

      mobile:
        codec: h264
        resolution: 480p
        bitrate: 1000kbps
        audio: aac_96

    adaptive_streaming:
      enabled: true
      protocols: [hls, dash]

  thumbnails:
    count: 10
    interval: auto
    sprite_sheet: true
```

**Document Processing:**

```yaml
document_pipeline:
  upload:
    max_size: 100MB
    allowed_types: [pdf, doc, docx, xls, xlsx, ppt, pptx]

  processing:
    pdf:
      generate_preview: true
      extract_text: true
      page_thumbnails: true

    office:
      convert_to_pdf: true
      extract_metadata: true

  security:
    virus_scan: true
    password_detection: true
```

### Step 6: Design Asset Metadata Model

**EF Core Model:**

```csharp
public class MediaAsset
{
    public Guid Id { get; set; }
    public string FileName { get; set; }
    public string ContentType { get; set; }
    public long FileSize { get; set; }
    public string StoragePath { get; set; }
    public MediaAssetType Type { get; set; }
    public MediaStatus Status { get; set; }

    // Extracted metadata (JSON column)
    public MediaMetadata Metadata { get; set; }

    // Processed variants
    public List<MediaVariant> Variants { get; set; }

    // DAM features
    public List<string> Tags { get; set; }
    public string AltText { get; set; }
    public string Caption { get; set; }
    public string Copyright { get; set; }
    public FocalPoint FocalPoint { get; set; }

    // Audit
    public Guid UploadedById { get; set; }
    public DateTime UploadedAt { get; set; }
}

[Owned]
public class MediaMetadata
{
    // Image metadata
    public int? Width { get; set; }
    public int? Height { get; set; }
    public string ColorSpace { get; set; }

    // Video metadata
    public TimeSpan? Duration { get; set; }
    public string Codec { get; set; }
    public int? Bitrate { get; set; }

    // Document metadata
    public int? PageCount { get; set; }
    public string Author { get; set; }
    public string Title { get; set; }

    // EXIF data
    public DateTime? DateTaken { get; set; }
    public string CameraModel { get; set; }
    public GeoLocation Location { get; set; }
}

[Owned]
public class FocalPoint
{
    public decimal X { get; set; }  // 0-1
    public decimal Y { get; set; }  // 0-1
}
```

### Step 7: Generate CDN Configuration

**Azure Front Door:**

```yaml
cdn:
  provider: azure_front_door

  endpoints:
    - name: media
      origin: cms-media-public.blob.core.windows.net

  rules:
    - name: images
      match:
        path: /images/*
      actions:
        cache_ttl: 7_days
        compression: true

    - name: transform
      match:
        path: /transform/*
      actions:
        origin_override: image-transform-function.azurewebsites.net

  security:
    waf: enabled
    rate_limiting: 1000/minute
    geo_filtering:
      allowed: [US, CA, EU]
```

## API Endpoints

```yaml
api:
  upload:
    - POST /api/media/upload
    - POST /api/media/upload/chunk (for large files)

  retrieve:
    - GET /api/media/{id}
    - GET /api/media/{id}/variants
    - GET /api/media/{id}/download

  transform:
    - GET /media/transform/{id}?w=800&h=600&fit=cover&format=webp

  search:
    - GET /api/media?tags=product&type=image

  manage:
    - PATCH /api/media/{id}/metadata
    - DELETE /api/media/{id}
```

## Related Skills

- `media-asset-management` - DAM patterns
- `image-optimization` - Responsive images
- `cdn-media-delivery` - CDN configuration
