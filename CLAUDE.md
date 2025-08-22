# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal blog built with Astro and the astro-pure theme. It features a bilingual design (Chinese/English) with custom fonts, blog analysis tools, and content generation scripts.

## Development Commands

```bash
# Start development server
npm run dev

# Development with type checking
npm run dev:check

# Build for production
npm run build

# Preview production build
npm run preview

# Type checking
npm run check

# Linting and formatting
npm run lint
npm run format
npm run yijiansilian  # Combined lint, sync, check, and format

# Clean build artifacts
npm run clean

# Content generation
python scripts/generate_new_post.py "Article Title" --mode file
python scripts/generate_new_post.py "Article Title" --mode dir
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

The `scripts/` directory contains Python tools for analyzing blog content:

### Setup
```bash
cd scripts
pip install -r requirements.txt
export DOUBAO_API_KEY=your_api_key_here
```

### Usage
```bash
# Run blog analysis
python blog_analysis.py

# Integrate analysis results to About page
python integrate_analysis_to_about.py output/blog_analysis_YYYYMMDD_HHMMSS.json
```

### Features
- Automatic blog discovery and text analysis
- AI-powered writing style and personality analysis  
- Caching system for incremental updates
- Integration with About page display

## Font System

The project uses a multi-font strategy:
- **LXGWWenKai**: Chinese content (elegant serif style)
- **Satoshi**: English content (modern sans-serif)
- **Monospace**: Code blocks

Fonts are preloaded and configured with fallback strategies. Use UnoCSS classes:
- `font-wenkai`: Chinese text
- `font-satoshi`: English text  
- `font-mono`: Code

## Markdown Features

Enhanced markdown processing includes:
- **Math**: KaTeX support via remark-math and rehype-katex
- **Code**: Syntax highlighting with copy buttons, diff notation, line highlighting
- **Headings**: Auto-generated anchor links
- **Images**: Sharp image processing with zoom functionality

## Deployment

The project is configured for static deployment. Build artifacts go to `dist/`. The README mentions syncing to a server via rsync:

```bash
rsync -avuz --progress --delete -e 'ssh -p 1202' dist/ root@server:/path/to/web/root
```

## Development Notes

- **Hot Reloading**: Use `npm run dev:check` for development with type checking
- **Content Types**: The theme supports both blog posts and documentation
- **Customization**: Main configuration in `src/site.config.ts`
- **Styling**: UnoCSS classes and custom CSS in `src/assets/styles/`
- **Scripts**: Python tools require API keys for AI analysis features

## Important Conventions

- Blog posts can be either single `.md` files or folders with `index.md`
- Images should be placed in the same folder as the post when using folder structure
- Use the `scripts/generate_new_post.py` tool for creating new posts
- All dates should be in ISO format in frontmatter
- Tags are automatically lowercased and deduplicated