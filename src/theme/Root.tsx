import {useEffect} from 'react';

/**
 * Root wrapper component
 *
 * 支持通过 URL 参数传递主题模式和嵌入模式：
 * - ?mode=dark 或 ?mode=light - 设置主题模式
 * - ?embed=true - 嵌入模式，隐藏导航栏和页脚
 * - ?lang=en 或 ?lang=zh - 语言会通过 URL 路径自动处理 (/en/docs/...)
 *
 * 示例：
 * - https://beecount.app/docs/intro?mode=dark&embed=true
 * - https://beecount.app/en/docs/intro?mode=light
 */
export default function Root({children}: {children: React.ReactNode}): React.ReactElement {
  useEffect(() => {
    // 客户端执行
    if (typeof window === 'undefined') return;

    const searchParams = new URLSearchParams(window.location.search);

    // 处理主题模式参数
    const mode = searchParams.get('mode');
    if (mode === 'dark' || mode === 'light') {
      // 设置 Docusaurus 的主题
      document.documentElement.setAttribute('data-theme', mode);
      // 保存到 localStorage
      localStorage.setItem('theme', mode);
    }

    // 处理嵌入模式
    const embed = searchParams.get('embed');
    if (embed === 'true' || embed === '1') {
      document.body.classList.add('embed-mode');
    }
  }, []);

  return <>{children}</>;
}
