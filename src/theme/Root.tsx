import React, {useEffect} from 'react';
import Head from '@docusaurus/Head';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

/**
 * Root wrapper component
 *
 * 支持通过 URL 参数传递主题模式和嵌入模式：
 * - ?mode=dark 或 ?mode=light - 设置主题模式
 * - ?embed=true - 嵌入模式，隐藏导航栏和页脚
 * - ?lang=en 或 ?lang=zh - 语言会通过 URL 路径自动处理 (/en/docs/...)
 *
 * 示例：
 * - https://count.beejz.com/docs/intro?mode=dark&embed=true
 * - https://count.beejz.com/en/docs/intro?mode=light
 */
export default function Root({children}: {children: React.ReactNode}): JSX.Element {
  const {i18n, siteConfig} = useDocusaurusContext();
  const isEn = i18n.currentLocale === 'en';
  const ogImage = `${siteConfig.url}/img/social-card${isEn ? '-en' : ''}.png`;

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'SoftwareApplication',
        name: isEn ? 'BeeCount' : '蜜蜂记账',
        alternateName: isEn ? '蜜蜂记账' : 'BeeCount',
        url: siteConfig.url,
        image: ogImage,
        description: isEn
          ? 'Open-source, free personal finance app for iOS, Android and Web. Simple, secure and private.'
          : '蜜蜂记账是一款开源免费的个人记账应用,支持 iOS、Android、Web。简洁易用,数据安全,支持多种云同步方式。',
        applicationCategory: 'FinanceApplication',
        operatingSystem: 'iOS, Android, Web',
        offers: {'@type': 'Offer', price: '0', priceCurrency: 'CNY'},
        author: {
          '@type': 'Organization',
          name: 'TNT-Likely',
          url: 'https://github.com/TNT-Likely',
        },
        downloadUrl: 'https://apps.apple.com/app/id6754611670',
      },
      {
        '@type': 'WebSite',
        name: isEn ? 'BeeCount' : '蜜蜂记账',
        url: siteConfig.url,
        inLanguage: isEn ? 'en' : 'zh-Hans',
        publisher: {'@type': 'Organization', name: 'TNT-Likely'},
      },
    ],
  };

  useEffect(() => {
    if (typeof window === 'undefined') return;

    const searchParams = new URLSearchParams(window.location.search);

    const mode = searchParams.get('mode');
    if (mode === 'dark' || mode === 'light') {
      document.documentElement.setAttribute('data-theme', mode);
      localStorage.setItem('theme', mode);
    }

    const embed = searchParams.get('embed');
    if (embed === 'true' || embed === '1') {
      document.body.classList.add('embed-mode');
    }
  }, []);

  return (
    <>
      <Head>
        <meta property="og:image" content={ogImage} />
        <meta name="twitter:image" content={ogImage} />
        <meta name="twitter:card" content="summary_large_image" />
        <meta property="og:type" content="website" />
        <meta property="og:site_name" content={isEn ? 'BeeCount' : '蜜蜂记账'} />
        <meta name="keywords" content={isEn
          ? 'BeeCount, personal finance, expense tracker, open source, free, iOS, Android, Web, budget app, money manager'
          : '蜜蜂记账, 记账, 个人记账, 开源记账, 免费记账, 记账软件, 记账APP, 自动记账, 预算管理, iOS记账, 安卓记账'} />
        <script type="application/ld+json">{JSON.stringify(jsonLd)}</script>
      </Head>
      {children}
    </>
  );
}
