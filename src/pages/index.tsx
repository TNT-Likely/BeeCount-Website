import clsx from 'clsx';
import {useEffect, useState} from 'react';
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

// 视频弹窗组件
function VideoModal({ isOpen, onClose }: { isOpen: boolean; onClose: () => void }) {
  useEffect(() => {
    if (isOpen) {
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = '';
    }
    return () => {
      document.body.style.overflow = '';
    };
  }, [isOpen]);

  if (!isOpen) return null;

  return (
    <div className={styles.videoModal} onClick={onClose}>
      <div className={styles.videoModalContent} onClick={(e) => e.stopPropagation()}>
        <button className={styles.videoModalClose} onClick={onClose}>×</button>
        <video
          className={styles.videoPlayer}
          controls
          autoPlay
          playsInline
        >
          <source src="/img/beecount-intro.mp4" type="video/mp4" />
        </video>
        <a
          href="https://m.bilibili.com/space/501149848"
          target="_blank"
          rel="noopener noreferrer"
          className={styles.videoCredit}
          onClick={(e) => e.stopPropagation()}
        >
          <svg className={styles.bilibiliIcon} viewBox="0 0 24 24" fill="currentColor">
            <path d="M17.813 4.653h.854c1.51.054 2.769.578 3.773 1.574 1.004.995 1.524 2.249 1.56 3.76v7.36c-.036 1.51-.556 2.769-1.56 3.773s-2.262 1.524-3.773 1.56H5.333c-1.51-.036-2.769-.556-3.773-1.56S.036 18.858 0 17.347v-7.36c.036-1.511.556-2.765 1.56-3.76 1.004-.996 2.262-1.52 3.773-1.574h.774l-1.174-1.12a1.234 1.234 0 0 1-.373-.906c0-.356.124-.659.373-.907l.027-.027c.267-.249.573-.373.92-.373.347 0 .653.124.92.373L9.653 4.44c.071.071.134.142.187.213h4.267a.836.836 0 0 1 .16-.213l2.853-2.747c.267-.249.573-.373.92-.373.347 0 .662.151.929.4.267.249.391.551.391.907 0 .355-.124.657-.373.906zM5.333 7.24c-.746.018-1.373.276-1.88.773-.506.498-.769 1.13-.786 1.894v7.52c.017.764.28 1.395.786 1.893.507.498 1.134.756 1.88.773h13.334c.746-.017 1.373-.275 1.88-.773.506-.498.769-1.129.786-1.893v-7.52c-.017-.765-.28-1.396-.786-1.894-.507-.497-1.134-.755-1.88-.773zM8 11.107c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c0-.373.129-.689.386-.947.258-.257.574-.386.947-.386zm8 0c.373 0 .684.124.933.373.25.249.383.569.4.96v1.173c-.017.391-.15.711-.4.96-.249.25-.56.374-.933.374s-.684-.125-.933-.374c-.25-.249-.383-.569-.4-.96V12.44c.017-.391.15-.711.4-.96.249-.249.56-.373.933-.373z"/>
          </svg>
          <Translate id="homepage.video.credit">视频来源: UP主 @星之墨辰</Translate>
        </a>
      </div>
    </div>
  );
}

// Hero 右侧的设备预览 —— mobile(双手机叠放)/ web(笔记本 + 浏览器 chrome)
// 5 秒自动切换,hover 暂停,底部指示点可手动切。两种形态尺寸相近(400x500),
// 切换时交叉 fade 而不是重排,避免 hero 高度抖动。
function DeviceShowcase() {
  const [mode, setMode] = useState<'mobile' | 'web'>('mobile');
  const [paused, setPaused] = useState(false);
  const {i18n} = useDocusaurusContext();
  const isZh = i18n.currentLocale === 'zh-Hans' || i18n.currentLocale === 'zh';
  const lang = isZh ? 'zh' : 'en';

  useEffect(() => {
    if (paused) return;
    const timer = setInterval(() => {
      setMode((prev) => (prev === 'mobile' ? 'web' : 'mobile'));
    }, 5000);
    return () => clearInterval(timer);
  }, [paused]);

  return (
    <div
      className={styles.deviceShowcase}
      onMouseEnter={() => setPaused(true)}
      onMouseLeave={() => setPaused(false)}
    >
      {/* Mobile 形态:原来的双手机叠放,保持不变。 */}
      <div
        className={clsx(styles.deviceView, styles.deviceViewMobile)}
        style={{ opacity: mode === 'mobile' ? 1 : 0, pointerEvents: mode === 'mobile' ? 'auto' : 'none' }}
        aria-hidden={mode !== 'mobile'}
      >
        <div className={styles.phoneShowcase}>
          <div className={styles.phoneFrame}>
            <img src="/img/preview/zh/01-home.png" alt={translate({id: 'homepage.hero.preview.home', message: '首页'})} className={styles.phoneScreen} />
          </div>
          <div className={clsx(styles.phoneFrame, styles.phoneFrameBack)}>
            <img src="/img/preview/dark/01-home.png" alt={translate({id: 'homepage.hero.preview.homeDark', message: '首页暗黑'})} className={styles.phoneScreen} />
          </div>
        </div>
      </div>

      {/* Web 形态:浏览器 chrome(traffic lights + URL bar)+ Web 仪表盘截图。 */}
      <div
        className={clsx(styles.deviceView, styles.deviceViewWeb)}
        style={{ opacity: mode === 'web' ? 1 : 0, pointerEvents: mode === 'web' ? 'auto' : 'none' }}
        aria-hidden={mode !== 'web'}
      >
        <div className={styles.browserFrame}>
          <div className={styles.browserChrome}>
            <div className={styles.browserDots}>
              <span style={{ background: '#ff5f56' }} />
              <span style={{ background: '#ffbd2e' }} />
              <span style={{ background: '#27c93f' }} />
            </div>
            <div className={styles.browserUrl}>beecount.local · Dashboard</div>
          </div>
          <img
            src={`/img/preview/web/${lang}-01-home.png`}
            alt={translate({id: 'homepage.hero.preview.web', message: 'Web 仪表盘'})}
            className={styles.browserScreen}
          />
        </div>
      </div>

      {/* 指示点 + label,点击切换。位置在右侧预览下方。 */}
      <div className={styles.deviceTabs}>
        <button
          type="button"
          className={clsx(styles.deviceTab, mode === 'mobile' && styles.deviceTabActive)}
          onClick={() => setMode('mobile')}
        >
          <Translate id="homepage.hero.device.mobile">Mobile</Translate>
        </button>
        <button
          type="button"
          className={clsx(styles.deviceTab, mode === 'web' && styles.deviceTabActive)}
          onClick={() => setMode('web')}
        >
          <Translate id="homepage.hero.device.web">Web</Translate>
        </button>
      </div>
    </div>
  );
}

// 全屏 Hero 区域 - 第一屏（极简版 + 预览图）
function HeroSection() {
  const [showVideo, setShowVideo] = useState(false);

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

          {/* 观看视频链接 */}
          <a className={styles.videoLink} onClick={() => setShowVideo(true)}>
            <svg className={styles.playIcon} viewBox="0 0 24 24" fill="currentColor">
              <path d="M8 5v14l11-7z"/>
            </svg>
            <Translate id="homepage.hero.watchVideo">观看介绍视频</Translate>
          </a>

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
              href="https://play.google.com/store/apps/details?id=com.tntlikely.beecount"
              className={styles.btnPrimary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M3,20.5V3.5C3,2.91 3.34,2.39 3.84,2.15L13.69,12L3.84,21.85C3.34,21.6 3,21.09 3,20.5M16.81,15.12L6.05,21.34L14.54,12.85L16.81,15.12M20.16,10.81C20.5,11.08 20.75,11.5 20.75,12C20.75,12.5 20.53,12.9 20.18,13.18L17.89,14.5L15.39,12L17.89,9.5L20.16,10.81M6.05,2.66L16.81,8.88L14.54,11.15L6.05,2.66Z"/>
              </svg>
              Google Play
            </a>
            <a
              href="https://github.com/TNT-Likely/BeeCount/releases/latest"
              className={styles.btnSecondary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M17.523 15.341a.91.91 0 100 1.82.91.91 0 000-1.82zm-11.046 0a.91.91 0 100 1.82.91.91 0 000-1.82zM12 2C6.477 2 2 6.477 2 12c0 4.42 2.865 8.166 6.839 9.489.5.092.682-.217.682-.482 0-.237-.008-.866-.013-1.7-2.782.603-3.369-1.342-3.369-1.342-.454-1.155-1.11-1.462-1.11-1.462-.908-.62.069-.608.069-.608 1.003.07 1.531 1.03 1.531 1.03.892 1.529 2.341 1.087 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.11-4.555-4.943 0-1.091.39-1.984 1.029-2.683-.103-.253-.446-1.27.098-2.647 0 0 .84-.269 2.75 1.025A9.578 9.578 0 0112 6.836c.85.004 1.705.114 2.504.336 1.909-1.294 2.747-1.025 2.747-1.025.546 1.377.203 2.394.1 2.647.64.699 1.028 1.592 1.028 2.683 0 3.842-2.339 4.687-4.566 4.935.359.309.678.919.678 1.852 0 1.336-.012 2.415-.012 2.743 0 .267.18.578.688.48C19.138 20.163 22 16.418 22 12c0-5.523-4.477-10-10-10z"/>
              </svg>
              Android APK
            </a>
            {/* Web 端:3.0 起 BeeCount Cloud 自带的浏览器版。没有公开 demo,
                链到 Cloud 仓库引导用户一键 docker compose 起来。 */}
            <a
              href="https://github.com/TNT-Likely/BeeCount-Cloud"
              className={styles.btnSecondary}
              target="_blank"
              rel="noopener noreferrer">
              <svg className={styles.btnIcon} viewBox="0 0 24 24" fill="currentColor">
                <path d="M3 4a2 2 0 0 0-2 2v10a2 2 0 0 0 2 2h6v2H7v2h10v-2h-2v-2h6a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2H3Zm0 2h18v10H3V6Z"/>
              </svg>
              <Translate id="homepage.hero.webButton">Web 版</Translate>
            </a>
          </div>
        </div>

        {/* 右侧:设备预览 —— mobile ↔ web 自动切换 */}
        <div className={styles.heroRight}>
          <DeviceShowcase />
        </div>
      </div>

      {/* 滚动提示 */}
      <div className={styles.scrollHint}>
        <span><Translate id="homepage.hero.scrollHint">向下滚动了解更多</Translate></span>
        <div className={styles.scrollArrow}>↓</div>
      </div>

      {/* 视频弹窗 */}
      <VideoModal isOpen={showVideo} onClose={() => setShowVideo(false)} />
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
      desc: '应用锁 + 生物识别\n多任务自动模糊屏幕',
    },
    {
      icon: '☁️',
      titleId: 'homepage.features.sync.title',
      title: '多端实时同步',
      descId: 'homepage.features.sync.desc',
      desc: 'BeeCount Cloud 自建云\niCloud / WebDAV / S3 任选',
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

// Web 端展示
function WebShowcaseSection() {
  const {i18n} = useDocusaurusContext();
  const isZh = i18n.currentLocale === 'zh-Hans' || i18n.currentLocale === 'zh';
  const lang = isZh ? 'zh' : 'en';

  return (
    <section className={styles.webShowcase}>
      <div className={styles.container}>
        <Heading as="h2" className={styles.sectionTitle}>
          <Translate id="homepage.webShowcase.title">Web 端</Translate>
        </Heading>
        <p className={styles.sectionSubtitle}>
          <Translate id="homepage.webShowcase.subtitle">
            3.0 起随 BeeCount Cloud 自带,浏览器直接用;PWA 装到桌面/Dock 像原生 app
          </Translate>
        </p>

        <div className={styles.webShowcaseGrid}>
          <div className={styles.webShowcaseItem}>
            <img
              src={`/img/preview/web/${lang}-01-home.png`}
              alt={translate({id: 'homepage.webShowcase.alt.home', message: 'Web 仪表盘'})}
            />
            <p className={styles.webShowcaseCaption}>
              <Translate id="homepage.webShowcase.caption.home">
                💰 仪表盘:收支、资产构成、分类热力、趋势一屏总览
              </Translate>
            </p>
          </div>
          <div className={styles.webShowcaseItem}>
            <img
              src={`/img/preview/web/${lang}-02-transactions.png`}
              alt={translate({id: 'homepage.webShowcase.alt.transactions', message: 'Web 交易列表'})}
            />
            <p className={styles.webShowcaseCaption}>
              <Translate id="homepage.webShowcase.caption.transactions">
                📒 交易列表:关键字 / 分类 / 账户 / 日期 / 标签多维筛选
              </Translate>
            </p>
          </div>
        </div>

        <div className={styles.webShowcaseCta}>
          <a
            href="https://github.com/TNT-Likely/BeeCount-Cloud"
            className={styles.btnPrimary}
            target="_blank"
            rel="noopener noreferrer">
            <Translate id="homepage.webShowcase.btn">一键自建 Docker 镜像</Translate>
          </a>
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
                <span className={styles.statNum}>1000+</span>
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


// 捐赠支持
function DonateSection() {
  const {i18n} = useDocusaurusContext();
  const isZh = i18n.currentLocale === 'zh-Hans' || i18n.currentLocale === 'zh';
  const donateUrl = isZh
    ? 'https://github.com/TNT-Likely/BeeCount/blob/main/docs/donate/README_ZH.md'
    : 'https://github.com/TNT-Likely/BeeCount/blob/main/docs/donate/README_EN.md';

  return (
    <section className={styles.donate}>
      <div className={styles.container}>
        <div className={styles.donateContent}>
          <div className={styles.donateIcon}>💝</div>
          <div className={styles.donateText}>
            <h3><Translate id="homepage.donate.title">支持项目</Translate></h3>
            <p>
              <Translate id="homepage.donate.desc">
                蜜蜂记账是完全免费开源的项目，没有广告和付费功能。如果您觉得有帮助，欢迎捐赠支持项目持续发展。
              </Translate>
            </p>
          </div>
          <a
            href={donateUrl}
            className={styles.donateBtn}
            target="_blank"
            rel="noopener noreferrer">
            <Translate id="homepage.donate.btn">了解捐赠方式</Translate>
          </a>
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
        <WebShowcaseSection />
        <CommunitySection />
        <DonateSection />
      </main>
    </Layout>
  );
}
