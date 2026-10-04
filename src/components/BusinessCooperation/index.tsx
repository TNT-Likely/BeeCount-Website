import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import Heading from '@theme/Heading';
import styles from './styles.module.css';

export function CooperationCards({detailed = false}: {detailed?: boolean}) {
  const options = [
    {
      title: translate({id: 'business.ai.title', message: 'AI 服务合作'}),
      description: translate({id: 'business.ai.description', message: '优先欢迎合规的 AI 模型与 API 服务商，让智能记账更易用。'}),
      detail: translate({id: 'business.ai.detail', message: '可洽谈用户专属额度与优惠、推广分成、项目赞助，以及接入适配、模型测试、联合教程与推广。'}),
    },
    {
      title: translate({id: 'business.website.title', message: '官网品牌展示'}),
      description: translate({id: 'business.website.description', message: '通过官网赞助卡片与品牌展示，连接关注记账和数据自主的用户。'}),
      detail: translate({id: 'business.website.detail', message: '可按展示位置、合作期限和内容形式洽谈，也可与 README 展示组合合作。'}),
    },
    {
      title: translate({id: 'business.readme.title', message: 'README 品牌展示'}),
      description: translate({id: 'business.readme.description', message: '在 GitHub 项目的赞助商区域，向开发者和自托管用户介绍你的品牌。'}),
      detail: translate({id: 'business.readme.detail', message: '可展示品牌 Logo、简短介绍和链接，具体位置与期限通过邮件确认。'}),
    },
  ];

  return (
    <div className={styles.cards}>
      {options.map((option, index) => (
        <article key={option.title} className={`${styles.card} ${index === 0 ? styles.featured : ''}`}>
          <div className={styles.cardTop}>
            <span className={styles.number} aria-hidden="true">0{index + 1}</span>
            {index === 0 && <span className={styles.badge}><Translate id="business.priority">优先合作</Translate></span>}
          </div>
          <Heading as="h3">{option.title}</Heading>
          <p>{option.description}</p>
          {detailed && <p className={styles.detail}>{option.detail}</p>}
        </article>
      ))}
    </div>
  );
}

export default function BusinessCooperation() {
  return (
    <section className={styles.section} data-business-section aria-labelledby="business-heading">
      <div className={styles.container}>
        <Heading as="h2" id="business-heading"><Translate id="business.title">商务合作</Translate></Heading>
        <p className={styles.intro}><Translate id="business.intro">与蜜蜂记账一起，让智能记账更易用，支持项目持续发展。</Translate></p>
        <CooperationCards />
        <div className={styles.actions}>
          <Link className={styles.primaryButton} to="/business"><Translate id="business.learnMore">了解合作方式</Translate><span aria-hidden="true"> →</span></Link>
          <span className={styles.note}><Translate id="business.scope">品牌展示限于官网与 README，App 内保持无广告。</Translate></span>
        </div>
      </div>
    </section>
  );
}
