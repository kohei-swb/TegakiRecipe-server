"use client"; // ← これを追加

export default function Home() {
  return (
    <div style={{ padding: '20px' }}>
      <h1>TegakiRecipe Debug Panel</h1>
      <p>ここにバックエンドとの通信結果を表示させます。</p>
      
      <button onClick={() => alert('ボタンが押されました')}>
        テストボタン
      </button>
    </div>
  );
}