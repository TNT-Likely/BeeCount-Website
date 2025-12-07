import clsx from 'clsx';
import {useEffect} from 'react';
import Link from '@docusaurus/Link';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import Translate, {translate} from '@docusaurus/Translate';

import styles from './index.module.css';

// 滚动显示/隐藏导航栏
function useScrollNavbar() {
  useEffect(() => {
    const navbar = document.querySelector('.navbar') as HTMLElement;
    if (!navbar) return;

    // 初始完全隐藏
    navbar.style.display = 'none';

    const handleScroll = () => {
      const scrollY = window.scrollY;
      const viewportHeight = window.innerHeight;

      // 滚动超过 80% 第一屏高度时显示导航栏
      if (scrollY > viewportHeight * 0.8) {
        navbar.style.display = '';
        navbar.style.opacity = '1';
      } else {
        navbar.style.display = 'none';
      }
    };

    window.addEventListener('scroll', handleScroll, { passive: true });
    handleScroll(); // 初始检查

    return () => {
      window.removeEventListener('scroll', handleScroll);
      // 恢复导航栏
      navbar.style.display = '';
      navbar.style.opacity = '';
    };
  }, []);
}

// 全屏 Hero 区域 - 第一屏（极简版 + 预览图）
function HeroSection() {
  return (
    <section className={styles.hero}>
      {/* 背景装饰 */}
      <div className={styles.heroBg}>
        <div className={styles.heroGradient} />
        <div className={styles.heroPattern} />
        {/* 粒子动画 */}
        <div className={styles.particles}>
          {[...Array(50)].map((_, i) => (
            <div key={i} className={styles.particle} style={{
              '--x': `${Math.random() * 100}%`,
              '--y': `${Math.random() * 100}%`,
              '--duration': `${3 + Math.random() * 4}s`,
              '--delay': `${Math.random() * 5}s`,
              '--size': `${2 + Math.random() * 4}px`,
              '--opacity': `${0.3 + Math.random() * 0.5}`,
            } as React.CSSProperties} />
          ))}
        </div>
        {/* 流星效果 */}
        <div className={styles.meteors}>
          {[...Array(6)].map((_, i) => (
            <div key={i} className={styles.meteor} style={{
              '--delay': `${i * 2.5}s`,
              '--left': `${10 + i * 15}%`,
            } as React.CSSProperties} />
          ))}
        </div>
      </div>

      <div className={styles.heroContent}>
        {/* 左侧：内容 */}
        <div className={styles.heroLeft}>
          {/* 第一行：Logo + 应用名称 */}
          <div className={styles.heroBrand}>
            <div className={styles.heroLogo}>
              <img src="/img/logo.svg" alt="BeeCount" />
            </div>
            <Heading as="h1" className={styles.heroTitle}>
              <span className={styles.heroTitleMain}>
                <Translate id="homepage.hero.title">蜜蜂记账</Translate>
              </span>
              <span className={styles.heroTitleSub}>BeeCount</span>
            </Heading>
          </div>

          {/* 第二行：Slogan */}
          <p className={styles.heroSlogan}>
            <Translate id="homepage.hero.slogan">你的数据，你做主的开源记账应用</Translate>
          </p>

          {/* 第三行：下载按钮 */}
          <div className={styles.heroButtons}>
            <a
              href="https://apps.apple.com/app/id6754611670"
              className={styles.btnPrimary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
              </svg>
              App Store
            </a>
            <a
              href="https://testflight.apple.com/join/Eaw2rWxa"
              className={styles.btnSecondary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M18.71 19.5c-.83 1.24-1.71 2.45-3.05 2.47-1.34.03-1.77-.79-3.29-.79-1.53 0-2 .77-3.27.82-1.31.05-2.3-1.32-3.14-2.53C4.25 17 2.94 12.45 4.7 9.39c.87-1.52 2.43-2.48 4.12-2.51 1.28-.02 2.5.87 3.29.87.78 0 2.26-1.07 3.81-.91.65.03 2.47.26 3.64 1.98-.09.06-2.17 1.28-2.15 3.81.03 3.02 2.65 4.03 2.68 4.04-.03.07-.42 1.44-1.38 2.83M13 3.5c.73-.83 1.94-1.46 2.94-1.5.13 1.17-.34 2.35-1.04 3.19-.69.85-1.83 1.51-2.95 1.42-.15-1.15.41-2.35 1.05-3.11z"/>
              </svg>
              TestFlight
            </a>
            <a
              href="https://github.com/TNT-Likely/BeeCount/releases/latest"
              className={styles.btnSecondary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.523 15.341a.91.91 0 100 1.82.91.91 0 000-1.82zm-11.046 0a.91.91 0 100 1.82.91.91 0 000-1.82zM12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.342-3.369-1.342-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
              </svg>
              Android
            </a>
          </div>
        </div>

        {/* 右侧：手机预览图 */}
        <div className={styles.heroRight}>
          <div className={styles.phoneShowcase}>
            <div className={styles.phoneFrame}>
              <img src="/img/preview/zh/01-home.png" alt={translate({id: 'homepage.hero.preview.home', message: '首页'})} className={styles.phoneScreen} />
            </div>
            <div className={clsx(styles.phoneFrame, styles.phoneFrameBack)}>
              <img src="/img/preview/dark/01-home.png" alt={translate({id: 'homepage.hero.preview.homeDark', message: '首页暗黑'})} className={styles.phoneScreen} />
            </div>
          </div>
        </div>
      </div>

      {/* 滚动提示 */}
      <div className={styles.scrollHint}>
        <span><Translate id="homepage.hero.scrollHint">向下滚动了解更多</Translate></span>
        <div className={styles.scrollArrow}>↓</div>
      </div>
    </section>
  );
}

// 功能亮点
function FeaturesSection() {
  const features = [
    {
      icon: '🤖',
      titleId: 'homepage.features.ai.title',
      title: 'AI 智能记账',
      descId: 'homepage.features.ai.desc',
      desc: '语音、图片、对话记账\n智能识别金额和分类',
    },
    {
      icon: '🔒',
      titleId: 'homepage.features.privacy.title',
      title: '隐私安全',
      descId: 'homepage.features.privacy.desc',
      desc: '数据本地存储\n完全掌控自己的数据',
    },
    {
      icon: '☁️',
      titleId: 'homepage.features.sync.title',
      title: '多端同步',
      descId: 'homepage.features.sync.desc',
      desc: 'iCloud / WebDAV / S3\n支持自建服务器',
    },
    {
      icon: '📊',
      titleId: 'homepage.features.stats.title',
      title: '统计分析',
      descId: 'homepage.features.stats.desc',
      desc: '收支趋势图表\n分类占比一目了然',
    },
    {
      icon: '📚',
      titleId: 'homepage.features.ledger.title',
      title: '多账本管理',
      descId: 'homepage.features.ledger.desc',
      desc: '日常、旅行、项目\n多场景独立管理',
    },
    {
      icon: '🏷️',
      titleId: 'homepage.features.budget.title',
      title: '标签与预算',
      descId: 'homepage.features.budget.desc',
      desc: '灵活标签分类\n预算提醒控制支出',
    },
    {
      icon: '🔄',
      titleId: 'homepage.features.recurring.title',
      title: '周期记账',
      descId: 'homepage.features.recurring.desc',
      desc: '自动记录固定支出\n房租水电不再遗漏',
    },
    {
      icon: '📱',
      titleId: 'homepage.features.auto.title',
      title: '自动记账',
      descId: 'homepage.features.auto.desc',
      desc: 'iOS 快捷指令\nAndroid 截图识别',
    },
    {
      icon: '💳',
      titleId: 'homepage.features.account.title',
      title: '账户管理',
      descId: 'homepage.features.account.desc',
      desc: '多账户余额追踪\n转账自动平账',
    },
  ];

  return (
    <section className={styles.features}>
      <div className={styles.container}>
        <Heading as="h2" className={styles.sectionTitle}>
          <Translate id="homepage.features.title">功能亮点</Translate>
        </Heading>
        <div className={styles.featureGrid}>
          {features.map((f, i) => (
            <div key={i} className={styles.featureCard}>
              <div className={styles.featureCardIcon}>{f.icon}</div>
              <h3><Translate id={f.titleId}>{f.title}</Translate></h3>
              <p><Translate id={f.descId}>{f.desc}</Translate></p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}

// 截图展示
function ScreenshotSection() {
  return (
    <section className={styles.screenshots}>
      <div className={styles.container}>
        <Heading as="h2" className={styles.sectionTitle}>
          <Translate id="homepage.screenshots.title">应用预览</Translate>
        </Heading>
        <p className={styles.sectionSubtitle}>
          <Translate id="homepage.screenshots.subtitle">精心设计的界面，支持亮色与暗黑模式</Translate>
        </p>

        <div className={styles.screenshotRow}>
          <img src="/img/preview/zh/01-home.png" alt={translate({id: 'homepage.screenshots.alt.home', message: '首页'})} />
          <img src="/img/preview/zh/04-chart-analysis.png" alt={translate({id: 'homepage.screenshots.alt.stats', message: '统计'})} />
          <img src="/img/preview/zh/14-discover.png" alt={translate({id: 'homepage.screenshots.alt.discover', message: '发现'})} />
          <img src="/img/preview/zh/03-edit-transaction.png" alt={translate({id: 'homepage.screenshots.alt.record', message: '记账'})} />
          <img src="/img/preview/dark/01-home.png" alt={translate({id: 'homepage.screenshots.alt.homeDark', message: '暗黑首页'})} />
          <img src="/img/preview/dark/05-ai-chat.png" alt={translate({id: 'homepage.screenshots.alt.aiChat', message: 'AI对话'})} />
        </div>
      </div>
    </section>
  );
}

// 开源社区
function CommunitySection() {
  return (
    <section className={styles.community}>
      <div className={styles.container}>
        <div className={styles.communityContent}>
          <div className={styles.communityLeft}>
            <Heading as="h2">
              <Translate id="homepage.community.title">开源项目</Translate>
            </Heading>
            <p>
              <Translate id="homepage.community.desc1">蜜蜂记账完全开源，代码托管在 GitHub。</Translate><br/>
              <Translate id="homepage.community.desc2">无广告、无会员、无隐藏收费。</Translate><br/>
              <Translate id="homepage.community.desc3">欢迎 Star 支持，一起让它变得更好！</Translate>
            </p>
            <div className={styles.communityStats}>
              <div className={styles.statItem}>
                <span className={styles.statNum}>700+</span>
                <span className={styles.statLabel}>Stars</span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statNum}>100%</span>
                <span className={styles.statLabel}>
                  <Translate id="homepage.community.stats.openSource">开源</Translate>
                </span>
              </div>
              <div className={styles.statItem}>
                <span className={styles.statNum}>0</span>
                <span className={styles.statLabel}>
                  <Translate id="homepage.community.stats.ads">广告</Translate>
                </span>
              </div>
            </div>
            <a
              href="https://github.com/TNT-Likely/BeeCount"
              className={styles.btnPrimary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M12 0c-6.626 0-12 5.373-12 12 0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23.957-.266 1.983-.399 3.003-.404 1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576 4.765-1.589 8.199-6.086 8.199-11.386 0-6.627-5.373-12-12-12z"/>
              </svg>
              GitHub
            </a>
          </div>
          <div className={styles.communityRight}>
            <h3><Translate id="homepage.community.contact">联系作者</Translate></h3>
            <div className={styles.socialLinks}>
              <a href="#" className={styles.socialLink}>
                <span className={styles.socialIcon}>💬</span>
                <span><Translate id="homepage.community.wechat">微信: LinYiXiao_Sx</Translate></span>
              </a>
              <a href="https://xhslink.com/m/8K1ekg7EFOq" className={styles.socialLink} target="_blank" rel="noopener noreferrer">
                <span className={styles.socialIcon}>📕</span>
                <span><Translate id="homepage.community.xiaohongshu">小红书 @蜜蜂记账</Translate></span>
              </a>
              <a href="https://v.douyin.com/YG7tUweYYyQ/" className={styles.socialLink} target="_blank" rel="noopener noreferrer">
                <span className={styles.socialIcon}>🎵</span>
                <span><Translate id="homepage.community.douyin">抖音 @蜜蜂记账</Translate></span>
              </a>
            </div>
          </div>
        </div>
      </div>
    </section>
  );
}

export default function Home(): JSX.Element {
  useScrollNavbar();

  return (
    <Layout
      title={translate({id: 'homepage.seo.title', message: '蜜蜂记账 - 简洁安全的个人记账工具'})}
      description={translate({id: 'homepage.seo.description', message: '蜜蜂记账是一款开源免费的个人记账应用，支持 iOS 和 Android。简洁易用，数据安全，支持多种云同步方式。'})}
      wrapperClassName={styles.homeWrapper}>
      <HeroSection />
      <main>
        <FeaturesSection />
        <ScreenshotSection />
        <CommunitySection />
      </main>
    </Layout>
  );
}
