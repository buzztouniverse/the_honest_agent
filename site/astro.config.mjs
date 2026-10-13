// @ts-check
import { fileURLToPath } from 'node:url';
import { defineConfig } from 'astro/config';
import react from '@astrojs/react';
import starlight from '@astrojs/starlight';

// The design system lives in the report's source (ui/src/ds), outside this folder.
// It comes in only through the @ds alias, so moving the site elsewhere means changing it here.
const ds = fileURLToPath(new URL('../ui/src/ds', import.meta.url));

// The docs open in light mode, like the landing page, until the reader picks a theme.
// Starlight stores the choice under this key ('' means "auto"), so only a missing key is set.
const lightByDefault = `if (localStorage.getItem('starlight-theme') === null) localStorage.setItem('starlight-theme', 'light');`;

export default defineConfig({
  site: 'https://thehonestagent.dev',
  integrations: [
    starlight({
      title: 'honest-agent',
      logo: { src: './public/assets/robot.png', alt: 'The Honest Agent robot' },
      favicon: '/favicon.svg',
      // Only the tokens: the design system's base.css restyles html, body and links, which is
      // right for the landing page and the report but would fight Starlight's own styles.
      customCss: [
        '@ds/tokens/fonts.css',
        '@ds/tokens/colors.css',
        '@ds/tokens/typography.css',
        '@ds/tokens/spacing.css',
        './src/styles/docs.css',
      ],
      head: [{ tag: 'script', content: lightByDefault }],
      social: [{ icon: 'github', label: 'GitHub', href: 'https://github.com/jlcoto/the_honest_agent' }],
      editLink: { baseUrl: 'https://github.com/jlcoto/the_honest_agent/edit/main/site/' },
      sidebar: [
        { label: 'Overview', link: '/docs/' },
        { label: 'Getting started', link: '/docs/getting-started/' },
        { label: 'Connect your agent', link: '/docs/connect/' },
        { label: 'Writing evals', link: '/docs/writing-evals/' },
        { label: 'Running evals', link: '/docs/running-evals/' },
        { label: 'The report', link: '/docs/report/' },
        { label: 'Setting up alerts', link: '/docs/alerts/' },
        {
          label: 'Running it for a team',
          items: [
            { label: 'Overview', link: '/docs/team/' },
            { label: 'Store results in MotherDuck', link: '/docs/team/results-motherduck/' },
            { label: 'Store results in S3', link: '/docs/team/results-s3/' },
            { label: 'Host the report on Cloudflare', link: '/docs/team/report-cloudflare/' },
            { label: 'Host the report on AWS', link: '/docs/team/report-aws/' },
            { label: 'Run it in GitHub Actions', link: '/docs/team/ci/' },
          ],
        },
        {
          label: 'Reference',
          items: [
            { label: 'CLI commands', link: '/docs/reference/cli/' },
            { label: 'Config keys', link: '/docs/reference/config/' },
          ],
        },
      ],
    }),
    react(),
  ],
  vite: {
    // dedupe: one React even when ui/node_modules has its own copy.
    resolve: { alias: { '@ds': ds }, dedupe: ['react', 'react-dom'] },
    server: { fs: { allow: ['..'] } },
  },
});
