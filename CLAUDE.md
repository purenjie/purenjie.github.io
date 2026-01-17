# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog built with Astro and the astro-pure theme. It features a bilingual design (Chinese/English) with custom fonts, blog analysis tools, and content generation scripts.

## Development Commands

```bash
# Start development server
npm run dev

# Development with type checking (runs check and dev in parallel)
npm run dev:check

# Build for production (runs astro-pure check, astro check, then build)
npm run build

# Preview production build
npm run preview

# Type checking
npm run check

# Sync Astro content collections
npm run sync

# Linting and formatting
npm run lint
npm run format
npm run yijiansilian  # Combined: lint, sync, check, and format (uses bun)

# Clean build artifacts
npm run clean

# astro-pure CLI commands
npm run pure          # Run astro-pure CLI
npm run new           # Create new content (alias for astro-pure new)

# Content generation (Python scripts)
python scripts/generate_new_post.py "Article Title" --mode file
python scripts/generate_new_post.py "Article Title" --mode dir
python scripts/generate_cover_image.py  # Generate cover images for posts
python scripts/extract_chinese_chars.py  # Extract Chinese characters for font subsetting
python scripts/subset_font.py            # Create font subsets
```

## Project Architecture

### Core Technologies
- **Astro 5.8+**: Static site generator with content collections
- **astro-pure 1.3.1**: Custom theme providing layout and components
- **UnoCSS**: Atomic CSS framework for styling
- **TypeScript**: Type safety throughout the project
- **Python Scripts**: Content analysis and generation tools

### Directory Structure

#### Content Organization
- `src/content/blog/`: Blog posts in Markdown/MDX format
  - Supports both single files (`.md`) and folder structure (`index.md` + assets)
  - Posts use frontmatter with title, description, publishDate, tags, heroImage
- `src/content/docs/`: Documentation pages (if enabled)

#### Key Configuration Files
- `src/site.config.ts`: Theme configuration, navigation, footer, integrations
- `src/content.config.ts`: Content collections schema definition
- `astro.config.ts`: Astro configuration with plugins and markdown settings
- `uno.config.ts`: UnoCSS configuration for styling

#### Components Architecture
- `src/components/about/`: About page specific components
- `src/components/home/`: Homepage components 
- `src/layouts/`: Page layout templates (BaseLayout, BlogPost, etc.)
- `src/pages/`: File-based routing structure

### Content Schema
Blog posts require these frontmatter fields:
- `title`: String (max 60 chars)
- `description`: String (max 160 chars)  
- `publishDate`: Date
- `tags`: Array of strings (lowercase, deduplicated)
- `heroImage`: Optional image object with src, alt, color properties
- `draft`: Boolean (default false)

## Blog Analysis Tools

The `scripts/ai_analysis/` directory contains a sophisticated AI-powered blog analysis system:

### Architecture
- **Map-Reduce Pattern**: Uses parallel processing to analyze individual posts (map phase) then aggregates insights (reduce phase)
- **LLM Integration**: Configured via `scripts/ai_analysis/llm.py` with support for various AI providers
- **Caching System**: Stores analysis results in `scripts/ai_analysis/cache/` for incremental updates
- **Schema Validation**: Uses Pydantic models in `scripts/ai_analysis/schema.py` for structured outputs

### Setup
```bash
cd scripts
pip install -r requirements.txt
export DOUBAO_API_KEY=your_api_key_here  # Or other LLM provider API key
```

### Usage
```bash
# Run full blog analysis (uses map-reduce pattern)
python -m ai_analysis.run

# The analysis generates a manifest.json with all post metadata
# Results are cached in ai_analysis/cache/ for efficiency
```

### Key Components
- `ai_analysis/run.py`: Main entry point orchestrating the analysis pipeline
- `ai_analysis/map_analyze.py`: Analyzes individual blog posts in parallel
- `ai_analysis/reduce_analyze.py`: Aggregates insights across all posts
- `ai_analysis/llm.py`: LLM client abstraction with retry logic (tenacity)
- `ai_analysis/config.py`: Configuration for analysis parameters
- `ai_analysis/utils.py`: Helper functions for file operations and text processing

## Font System

The project uses a multi-font strategy with font subsetting for performance:
- **LXGWWenKai (霞鹜文楷)**: Chinese content (elegant serif style)
- **Satoshi**: English content (modern sans-serif)
- **Monospace**: Code blocks

### Font Optimization
- Fonts are stored in `public/fonts/` and preloaded in the HTML head
- Use `scripts/extract_chinese_chars.py` to extract unique Chinese characters from blog posts
- Use `scripts/subset_font.py` to create optimized font subsets containing only used characters
- This reduces font file sizes significantly for faster page loads

### UnoCSS Font Classes
- `font-wenkai`: Chinese text
- `font-satoshi`: English text
- `font-mono`: Code blocks

Font configuration is defined in [uno.config.ts](uno.config.ts) with custom rules and fallback strategies.

## Markdown Features

Enhanced markdown processing configured in [astro.config.ts](astro.config.ts):

### Math Support
- **KaTeX**: Renders LaTeX math expressions via `remark-math` and `rehype-katex`
- Supports inline math `$...$` and display math `$$...$$`

### Code Highlighting
- **Shiki**: Syntax highlighting with `one-dark-pro` theme (light and dark)
- **Custom Transformers** (defined in `src/plugins/shiki-transformers.ts`):
  - `addCopyButton`: Adds copy-to-clipboard functionality (2s timeout)
  - `addLanguage`: Displays language label on code blocks
  - `addTitle`: Supports code block titles
  - `transformerNotationDiff`: Supports diff notation (`// [!code ++]` and `// [!code --]`)
  - `transformerNotationHighlight`: Supports line highlighting
  - `updateStyle`: Custom styling for code blocks

### Heading Links
- **Auto-generated anchors**: Via `rehype-auto-link-headings` plugin
- Anchor links appear on hover with `#` symbol
- Configured with `scroll-margin-top: 3rem` for proper scroll positioning

### Images
- **Sharp**: Image optimization and processing
- **Medium Zoom**: Click-to-zoom functionality on images with `.zoomable` class
- Images in prose content automatically get zoom capability

## Deployment

The project is configured for static site generation. Build artifacts are output to `dist/`.

### Deployment Options
The [astro.config.ts](astro.config.ts) includes commented adapter configurations for:
- **Vercel** (serverless or static)
- **Node.js** (standalone mode)
- **Static hosting** (current default)

### Server Deployment
Deploy to server via rsync (from README):
```bash
rsync -avuz --progress --delete -e 'ssh -p 1202' dist/ root@104.168.120.15:/opt/1panel/apps/openresty/openresty/www/sites/solejay.cn/index
```

## Theme Configuration

The astro-pure theme is configured via [src/site.config.ts](src/site.config.ts):

### Key Configuration Objects
- **`theme`**: Site metadata, locale, logo, header menu, footer, content settings
- **`integ`**: Integration settings (pagefind search, quote API, typography, mediumZoom, waline comments)
- **`terms`**: Terms and policy pages configuration

### Important Settings
- **Navigation**: Edit `theme.header.menu` array to modify site navigation
- **Footer**: Configure copyright, links, and social media in `theme.footer`
- **Typography**: Customize prose styles via `integ.typography` (blockquote style, inline code style)
- **Search**: Pagefind integration enabled via `integ.pagefind`
- **Comments**: Waline is currently disabled (`integ.waline.enable: false`)

## Styling System

### UnoCSS Configuration
The project uses UnoCSS (configured in [uno.config.ts](uno.config.ts)) with:
- **Preset Mini**: Core utility classes
- **Preset Typography**: Prose styling with extensive customizations
- **Custom Rules**: Font families, color schemes, and component styles

### Typography Customization
The prose styles include custom CSS for:
- **Headings**: Scroll margin, hover-visible anchor links, custom font weights
- **Blockquotes**: Custom borders, shadows, and decorative quotation marks
- **Code blocks**: Inline and block code styling (modern or traditional styles)
- **Links**: External link indicators and hover effects

### Color System
Uses CSS custom properties defined in the theme:
- `--foreground`, `--background`: Main colors
- `--muted-foreground`, `--muted`: Secondary colors
- `--primary`, `--secondary`, `--accent`: Theme colors
- All colors use HSL format for easy theming

### Custom Styles
Additional styles in `src/assets/styles/` for specific components and layouts.

## Important Conventions

- Blog posts can be either single `.md` files or folders with `index.md` (folder mode recommended for posts with images)
- Images should be placed in the same folder as the post when using folder structure
- Use `scripts/generate_new_post.py` for creating new posts (handles frontmatter template)
- All dates must be in ISO format (YYYY-MM-DD) in frontmatter
- Tags are automatically lowercased and deduplicated by the content schema
- The site is configured for `https://rojoey.github.io` (see `astro.config.ts` site setting)