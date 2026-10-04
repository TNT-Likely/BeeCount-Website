import Link from '@docusaurus/Link';
import Translate, {translate} from '@docusaurus/Translate';
import Layout from '@theme/Layout';
import Heading from '@theme/Heading';
import {CooperationCards} from '../components/BusinessCooperation';
import shared from '../components/BusinessCooperation/styles.module.css';
import styles from './business.module.css';

export default function BusinessPage() {
  const subject = translate({id: 'business.email.subject', message: 'BeeCount 商务合作咨询'});
  const body = translate({id: 'business.email.body', message: '品牌 / 公司：\n官网：\n合作方向：\n合作需求与用户权益：\n预算与合作期限：\n联系方式：\n'});
  const emailUrl = `mailto:sunxiaoyes@outlook.com?subject=${encodeURIComponent(subject)}&body=${encodeURIComponent(body)}`;

  return (
    <Layout title={translate({id: 'business.title', message: '商务合作'})} description={translate({id: 'business.seo.description', message: '蜜蜂记账商务合作：合规 AI 模型与 API 服务商合作、官网及 GitHub README 品牌展示。'})}>
      <main className={styles.page} data-business-section>
        <div className={shared.container}>
          <header className={styles.hero}>
            <span className={styles.eyebrow}>BEECOUNT · PARTNERSHIPS</span>
            <Heading as="h1"><Translate id="business.title">商务合作</Translate></Heading>
            <p className={shared.intro}><Translate id="business.intro">与蜜蜂记账一起，让智能记账更易用，支持项目持续发展。</Translate></p>
            <a className={shared.primaryButton} href="#contact"><Translate id="business.contactAction">洽谈合作</Translate><span aria-hidden="true"> ↗</span></a>
          </header>

          <section aria-labelledby="directions-heading">
            <Heading as="h2" id="directions-heading"><Translate id="business.directions">合作方向</Translate></Heading>
            <CooperationCards detailed />
          </section>

          <section className={styles.ecosystem} aria-labelledby="ecosystem-heading">
            <Heading as="h2" id="ecosystem-heading"><Translate id="business.ecosystem.title">项目赞助与生态共建</Translate></Heading>
            <p className={shared.note}><Translate id="business.ecosystem.intro">除了品牌展示，也欢迎通过长期支持和技术合作，共同改善真实的记账体验。</Translate></p>
            <div className={styles.ecosystemList}>
              <div className={styles.ecosystemItem}>
                <Heading as="h3"><Translate id="business.ecosystem.sponsor.title">长期项目赞助</Translate></Heading>
                <p><Translate id="business.ecosystem.sponsor.description">按季度或年度支持项目维护，可洽谈官网与 README 致谢及定期项目进展。赞助不设置用户功能付费墙，也不涉及用户数据。</Translate></p>
              </div>
              <div className={styles.ecosystemItem}>
                <Heading as="h3"><Translate id="business.ecosystem.deployment.title">Cloud 部署合作</Translate></Heading>
                <p><Translate id="business.ecosystem.deployment.description">欢迎云服务、NAS 与部署平台伙伴，共建一键安装、升级和备份方案，降低自建门槛，保留用户对部署环境的自主选择。</Translate></p>
              </div>
              <div className={styles.ecosystemItem}>
                <Heading as="h3"><Translate id="business.ecosystem.features.title">公共功能共建</Translate></Heading>
                <p><Translate id="business.ecosystem.features.description">可共同支持导入适配、无障碍等通用功能的开发，成果面向所有用户开放。开发范围、交付阶段与维护责任通过邮件商议。</Translate></p>
              </div>
            </div>
          </section>

          <section className={styles.principles} aria-labelledby="principles-heading">
            <Heading as="h2" id="principles-heading"><Translate id="business.principles.title">合作原则</Translate></Heading>
            <ul>
              <li><Translate id="business.principles.provider">优先选择主体、模型来源与服务授权清晰，计费及隐私政策透明的 AI 服务商；具体资质在合作前核验。</Translate></li>
              <li><Translate id="business.principles.fit">AI 合作以实际记账场景的适配效果和用户权益为基础，保留用户自主选择服务商的能力。</Translate></li>
              <li><Translate id="business.principles.transparency">付费品牌展示将明确标注广告或赞助，推广链接将说明合作关系，不接入第三方广告追踪脚本。</Translate></li>
              <li><Translate id="business.principles.privacy">合作不涉及出售或共享用户账本、API Key 等私人数据。App 内保持无广告。</Translate></li>
            </ul>
          </section>

          <section className={styles.contact} id="contact" aria-labelledby="contact-heading">
            <Heading as="h2" id="contact-heading"><Translate id="business.contact.title">聊聊你的合作想法</Translate></Heading>
            <p><Translate id="business.contact.description">请附上品牌或公司介绍、官网、合作方向、用户权益，以及预算与合作期限。具体展示位置、报价和合作条件通过邮件商议。</Translate></p>
            <a className={shared.primaryButton} href={emailUrl}><Translate id="business.contactAction">洽谈合作</Translate></a>
            <a className={styles.email} href={emailUrl}>sunxiaoyes@outlook.com</a>
            <p className={shared.note}><Translate id="business.contact.other">商业授权、部署协助与定制开发，也欢迎通过此邮箱咨询。</Translate></p>
          </section>
        </div>
      </main>
      <div className={styles.embedNotice} data-business-embed-notice>
        <p><Translate id="business.embedNotice">此页面面向官网访客。你可以继续查看蜜蜂记账使用文档。</Translate></p>
        <Link to="/docs/intro"><Translate id="business.backToDocs">查看使用文档</Translate></Link>
      </div>
    </Layout>
  );
}
