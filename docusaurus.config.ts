import {themes as prismThemes} from 'prism-react-renderer';
import type {Config} from '@docusaurus/types';
import type * as Preset from '@docusaurus/preset-classic';

const config: Config = {
  title: '蜜蜂记账',
  tagline: '简洁、安全、可控的个人记账工具',
  favicon: 'img/favicon.ico',

  url: 'https://beecount.app',
  baseUrl: '/',

  organizationName: 'TNT-Likely',
  projectName: 'BeeCount',

  onBrokenLinks: 'throw',
  onBrokenMarkdownLinks: 'warn',

  i18n: {
    defaultLocale: 'zh-Hans',
    locales: ['zh-Hans', 'en'],
    localeConfigs: {
      'zh-Hans': {
        label: '简体中文',
        htmlLang: 'zh-Hans',
      },
      en: {
        label: 'English',
        htmlLang: 'en',
      },
    },
  },

  presets: [
    [
      'classic',
      {
        docs: {
          sidebarPath: './sidebars.ts',
          editUrl: 'https://github.com/TNT-Likely/BeeCount-Website/tree/main/',
        },
        blog: false,
        theme: {
          customCss: './src/css/custom.css',
        },
      } satisfies Preset.Options,
    ],
  ],

  themes: [
    [
      require.resolve("@easyops-cn/docusaurus-search-local"),
      {
        hashed: true,
        language: ["en", "zh"],
        highlightSearchTermsOnTargetPage: true,
        explicitSearchResultPath: true,
        docsRouteBasePath: "/docs",
        indexBlog: false,
      },
    ],
  ],

  themeConfig: {
    image: 'img/social-card.png',
    navbar: {
      title: '蜜蜂记账',
      logo: {
        alt: 'BeeCount Logo',
        src: 'img/logo.svg',
      },
      items: [
        {
          type: 'docSidebar',
          sidebarId: 'tutorialSidebar',
          position: 'left',
          label: '文档',
        },
        // {to: '/blog', label: '博客', position: 'left'},
        {
          to: '/donate',
          label: '捐赠',
          position: 'left',
        },
        {
          type: 'localeDropdown',
          position: 'right',
        },
        {
          href: 'https://github.com/TNT-Likely/BeeCount',
          label: 'GitHub',
          position: 'right',
        },
      ],
    },
    footer: {
      style: 'dark',
      links: [
        {
          title: '社区',
          items: [
            {
              label: 'GitHub',
              href: 'https://github.com/TNT-Likely/BeeCount',
            },
            {
              label: '小红书 @蜜蜂记账',
              href: 'https://xhslink.com/m/8K1ekg7EFOq',
            },
            {
              label: '抖音 @蜜蜂记账',
              href: 'https://v.douyin.com/YG7tUweYYyQ/',
            },
          ],
        },
        {
          title: '相关产品',
          items: [
            {
              html: `<a href="https://beedns.youths.cc" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.875rem 1rem; background: rgba(248, 201, 28, 0.08); border: 1px solid rgba(248, 201, 28, 0.2); border-radius: 10px; text-decoration: none; margin-top: 0.5rem;">
                <span style="font-size: 1.75rem; line-height: 1;">🐝</span>
                <span>
                  <span style="display: block; font-weight: 600; color: #F8C91C; margin-bottom: 0.25rem;">蜜蜂域名 BeeDNS</span>
                  <span style="display: block; font-size: 0.8em; color: rgba(255,255,255,0.6); line-height: 1.4;">简洁高效的 DNS 管理工具<br/>支持阿里云 DNS</span>
                </span>
              </a>`,
            },
            {
              html: `<a href="https://ziqu.youths.cc" target="_blank" rel="noopener noreferrer" style="display: flex; align-items: flex-start; gap: 0.75rem; padding: 0.875rem 1rem; background: rgba(45, 140, 111, 0.08); border: 1px solid rgba(45, 140, 111, 0.2); border-radius: 10px; text-decoration: none; margin-top: 0.5rem;">
                <span style="font-size: 1.75rem; line-height: 1;">🀄</span>
                <span>
                  <span style="display: block; font-weight: 600; color: #2d8c6f; margin-bottom: 0.25rem;">字趣 Ziqu</span>
                  <span style="display: block; font-size: 0.8em; color: rgba(255,255,255,0.6); line-height: 1.4;">好玩的中文汉字成语小游戏<br/>成语Wordle · 成语接龙 · 诗词填空</span>
                </span>
              </a>`,
            },
          ],
        },
        {
          title: '友情链接',
          items: [
            {
              label: '果核剥壳',
              href: 'https://www.ghxi.com/',
            },
            {
              label: 'B站 @星之墨辰',
              href: 'https://m.bilibili.com/space/501149848',
            },
          ],
        },
      ],
      copyright: `© ${new Date().getFullYear()} 蜜蜂记账 BeeCount`,
    },
    prism: {
      theme: prismThemes.github,
      darkTheme: prismThemes.dracula,
    },
    colorMode: {
      defaultMode: 'dark',
      disableSwitch: false,
      respectPrefersColorScheme: false,
    },
  } satisfies Preset.ThemeConfig,
};

export default config;
