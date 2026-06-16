---
title: "Containerize Your .NET Applications Without a Dockerfile"
slug: containerize-your-dotnet-applications-without-a-dockerfile
date: 2026-01-31
author: Milan Jovanovic
description: "Since .NET 7, the SDK can publish applications directly to container images without a Dockerfile. Learn how to configure image naming, base images, ports, and push to registries."
tags:
  - aspnet-core
  - docker
  - dotnet-10
  - ci-cd
source_url: https://www.milanjovanovic.tech/blog/containerize-your-dotnet-applications-without-a-dockerfile
doc_id: milanjovanovic-tech-blog-containerize-your-dotnet-applications-without-a-dockerfile
---

# Containerize Your .NET Applications Without a Dockerfile

Since .NET 7, developers can publish applications directly to container images using the SDK's built-in support, eliminating the need to maintain separate Dockerfile configurations.

## Key Capabilities

The traditional multi-stage Dockerfile approach requires understanding layer caching, base image selection, and proper file ordering. The SDK approach streamlines this by automating these decisions during the `dotnet publish` command with the `/t:PublishContainer` target.

## Basic Publishing

A single command handles containerization:

```bash
dotnet publish --os linux --arch x64 /t:PublishContainer
```

The SDK automatically selects appropriate base images (runtime-deps for self-contained apps, aspnet for ASP.NET Core, runtime for others) and loads the image into a local Docker daemon.

## Customization Options

**Image Naming**: Configure repository and tags via MSBuild properties in your `.csproj`:

- `ContainerRepository`: Sets the image registry location
- `ContainerImageTags`: Specifies one or more tags (semicolon-separated)

**Base Image Selection**: Switch to Alpine variants for smaller deployments. The default aspnet image is 231.73 MB while the Alpine version is 122.65 MB - approximately 47% smaller.

**Port Configuration**: Expose ports through `ContainerPort` items, with TCP/UDP type specification.

## Registry Publishing

Push to GitHub Container Registry by specifying the registry during publishing:

```bash
dotnet publish --os linux --arch x64 /t:PublishContainer /p:ContainerRegistry=ghcr.io
```

The author prefers using Docker CLI directly for greater control over authentication and tagging in CI/CD pipelines.

## Deployment Integration

The article demonstrates a GitHub Actions workflow that builds the container, tags it, pushes to a registry, and triggers deployment via Dokploy - a Docker deployment tool for VPS environments.

## Limitations

Traditional Dockerfiles remain necessary for:

- Installing system dependencies (native libraries like libgdiplus)
- Complex multi-stage custom build steps
- Non-.NET components requiring additional services

For standard web APIs and background services, the SDK approach is sufficient.
