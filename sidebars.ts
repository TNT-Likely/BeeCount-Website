import type {SidebarsConfig} from '@docusaurus/plugin-content-docs';

const sidebars: SidebarsConfig = {
  tutorialSidebar: [
    'intro',
    {
      type: 'category',
      label: '快速开始',
      items: ['getting-started/installation', 'getting-started/first-record'],
    },
    {
      type: 'category',
      label: '记账',
      items: [
        'record/basic',
        'record/recurring',
        'record/attachment',
        'record/auto-ios',
        'record/auto-android',
        'record/import-export',
        'record/quick-actions',
      ],
    },
    {
      type: 'category',
      label: '分类与标签',
      items: [
        'category/manage',
        'category/subcategory',
        'category/tag',
      ],
    },
    {
      type: 'category',
      label: '账户与账本',
      items: [
        'account/manage',
        'account/ledger',
        'account/budget',
      ],
    },
    {
      type: 'category',
      label: '统计分析',
      items: [
        'statistics/overview',
        'statistics/chart',
        'statistics/calendar',
      ],
    },
    {
      type: 'category',
      label: 'AI 助手',
      items: [
        'ai/overview',
        'ai/voice',
        'ai/image',
        'ai/chat',
      ],
    },
    {
      type: 'category',
      label: '云同步',
      items: [
        'cloud-sync/overview',
        'cloud-sync/icloud',
        'cloud-sync/supabase',
        'cloud-sync/webdav',
        'cloud-sync/s3',
      ],
    },
    {
      type: 'category',
      label: '个性化',
      items: [
        'personalize/theme',
        'personalize/dark-mode',
        'personalize/color-scheme',
      ],
    },
    'faq',
    'contributing',
    'changelog',
  ],
};

export default sidebars;
