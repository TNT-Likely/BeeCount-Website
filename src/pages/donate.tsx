import {useEffect} from 'react';
import useDocusaurusContext from '@docusaurus/useDocusaurusContext';

export default function DonatePage(): JSX.Element {
  const {i18n} = useDocusaurusContext();
  const isZh = i18n.currentLocale === 'zh-Hans' || i18n.currentLocale === 'zh';

  const donateUrl = isZh
    ? 'https://github.com/TNT-Likely/BeeCount/blob/main/docs/donate/README_ZH.md'
    : 'https://github.com/TNT-Likely/BeeCount/blob/main/docs/donate/README_EN.md';

  useEffect(() => {
    window.location.href = donateUrl;
  }, [donateUrl]);

  return null;
}
