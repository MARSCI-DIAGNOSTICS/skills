---
doc_id: milanjovanovic-tech-blog-the-new-slnx-solution-format-migration-guide
title: "The New .slnx Solution Format (migration guide)"
description: "See what changes in .slnx, how to convert your existing .sln, and what to watch out for in CI."
source_url: https://www.milanjovanovic.tech/blog/the-new-slnx-solution-format-migration-guide
published_at: "2025-12-13"
author: Milan Jovanović
---

# The New .slnx Solution Format (migration guide)

**Solution files** have always been _that one file_ nobody wants to touch during a **merge conflict**.
I still remember the pain of resolving conflicts in large monorepo solutions with hundreds of projects.
Can I just say this was not fun?

Microsoft is (finally!) addressing that with **`.slnx`**: an **XML-based**, simpler solution format designed to be easier to read, edit, and merge.

Here is your practical guide to the future of .NET solutions.

## The problem with `.sln`

Classic `.sln` files are verbose: GUID-heavy project entries + configuration blocks that explode as your solution grows.
It's also a frequent source of merge conflicts.

To appreciate the new format, we must look at the old one.

Here's a typical `.sln` file from a moderately sized .NET solution:

```txt
Microsoft Visual Studio Solution File, Format Version 12.00
# Visual Studio Version 17
VisualStudioVersion = 17.7.34031.279
MinimumVisualStudioVersion = 10.0.40219.1
Project("{2150E333-8FDC-42A3-9474-1A3956D46DE8}") = "Solution Items", "Solution Items", "{8FC526EA-218B-4615-8410-4E1850611F38}"
	ProjectSection(SolutionItems) = preProject
		.editorconfig = .editorconfig
		Directory.Build.props = Directory.Build.props
		Directory.Packages.props = Directory.Packages.props
	EndProjectSection
EndProject
Project("{2150E333-8FDC-42A3-9474-1A3956D46DE8}") = "src", "src", "{64A28C1B-09AF-426E-8721-D002BE554B48}"
EndProject
Project("{9A19103F-16F7-4668-BE54-9A1E7A4F7556}") = "SharedKernel", "src\SharedKernel\SharedKernel.csproj", "{166778A2-518F-47F0-BBC7-DB49C76A963C}"
EndProject
...
```

Good luck trying to make sense of that during a merge conflict!

## What `.slnx` looks like

A minimal `.slnx` is basically a list of projects in XML.

Here's the same solution as above, but in `.slnx` format.
We even have solution items, folders, and a docker-compose project.

```xml
<Solution>
  <Folder Name="/Solution Items/">
    <File Path=".editorconfig" />
    <File Path="Directory.Build.props" />
    <File Path="Directory.Packages.props" />
  </Folder>
  <Folder Name="/src/">
    <Project Path="src/Application/Application.csproj" />
    <Project Path="src/Domain/Domain.csproj" />
    <Project Path="src/Infrastructure/Infrastructure.csproj" />
    <Project Path="src/SharedKernel/SharedKernel.csproj" />
    <Project Path="src/Web.Api/Web.Api.csproj" />
  </Folder>
  <Folder Name="/tests/">
    <Project Path="tests/ArchitectureTests/ArchitectureTests.csproj" />
  </Folder>
  <Project Path="docker-compose.dcproj">
    <Build />
  </Project>
</Solution>
```

It looks remarkably similar to a `.csproj` file.

## How to Migrate Today

The `.slnx` format is available in recent versions of Visual Studio 2022 (v17.13+) and the .NET 9 SDK. Here is how you can switch.

**Option 1: The Command Line**

If you have the .NET 9 SDK installed (specifically 9.0.200 or later), you can migrate instantly via the CLI.

1. Open your terminal in the solution folder.

2. Run the migration command:

```bash
dotnet sln migrate
```

3. This creates a new `.slnx` file alongside your old `.sln`.

At this point I would recommend deleting the old `.sln` file to avoid confusion.
There's no point in keeping both in the same repo.

**Option 2: Visual Studio "Save As"**

If you prefer the GUI, you can do this directly inside Visual Studio 2022 (or 2026).

1. Select the Solution in the Solution Explorer.

2. Go to `File` > `Save Solution As...`.

3. Change the "Save as type" dropdown to Xml Solution File (*.slnx).

## Why You Should Care

- **Fewer Merge Conflicts**: The #1 benefit.
Because the file is simple XML without random GUIDs changing, git merges become trivial.
- **Human Readable**: You can open this in Notepad, understand it, and edit it without breaking your entire build.
- **Consistency**: It finally aligns the solution format with the project format (`.csproj`), which moved to simplified XML years ago.
- **Performance**: Smaller file sizes and simpler parsing mean slightly faster load times for massive solutions.

## Is it Ready?

As of late 2025/early 2026, `.slnx` is technically a **Preview** feature.

**Safe to use**?
Yes, the format is stable.

**Tooling support**?
Visual Studio 2022, Visual Studio 2026 and Rider support it well.
So does the .NET CLI.
Some older CI/CD pipelines or 3rd party tools might not recognize the extension yet.

**My recommendation**: Try it on a side project or a branch first.
If your CI pipeline passes, you are ready to modernize.

**I'm using this format** in all my new projects and have migrated several existing ones without issues.
