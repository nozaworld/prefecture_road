const routes = routeNames; // サーバーから渡された路線名リスト

const input = document.getElementById('routeInput'); // 入力欄
const suggestionBox = document.getElementById('suggestions'); // 候補リスト
const hiddenInput = document.querySelector('input[name="route_name"]'); // 隠し入力欄

let currentIndex = -1; // 現在選択中の候補のインデックス

// 候補リストを更新する関数
function updateSuggestions() {
    const keyword = input.value.trim();
    suggestionBox.innerHTML = '';
    currentIndex = -1;

    // キーワードにマッチする路線名をフィルタリング
    let matches = keyword === ''
    ? routes.slice()
    : routes.filter(r => r.includes(keyword));

    // 表示上限を設定
    const MAX_SHOW = 1000;
    // 候補をリストに追加
    matches.slice(0, MAX_SHOW).forEach(match => {
    const li = document.createElement('li');
    li.textContent = match;
    li.addEventListener('click', () => {
        input.value = match;
        suggestionBox.style.display = 'none';
    });
    suggestionBox.appendChild(li);
    });
    // 候補リストの表示/非表示を切り替え
    suggestionBox.style.display = matches.length > 0 ? 'block' : 'none';
}

// 入力欄の変化に応じて候補を更新
input.addEventListener('input', updateSuggestions);
// フォーカス時に候補を表示
input.addEventListener('focus', () => {
    if (input.value.trim() === '') updateSuggestions();
});

// 入力欄外をクリックしたら候補を非表示
document.addEventListener('click', (e) => {
    if (!suggestionBox.contains(e.target) && e.target !== input) {
    suggestionBox.style.display = 'none';
    }
});

// キーボード操作で候補を選択
input.addEventListener('keydown', (e) => {
    const items = suggestionBox.querySelectorAll('li');
    // 候補が表示されていない場合は何もしない
    if (suggestionBox.style.display === 'none' || items.length === 0) return;

    // 下矢印キーで候補を選択
    if (e.key === 'ArrowDown') {
    e.preventDefault();
    currentIndex = (currentIndex + 1) % items.length;
    highlightItem(items);
    // 上矢印キーで候補を選択
    } else if (e.key === 'ArrowUp') {
    e.preventDefault();
    currentIndex = (currentIndex - 1 + items.length) % items.length;
    highlightItem(items);
    // Enterキーで選択確定
    } else if (e.key === 'Enter') {
    if (currentIndex >= 0 && items[currentIndex]) {
        // 選択中の候補を入力欄に設定
        e.preventDefault();
        input.value = items[currentIndex].textContent;
        suggestionBox.style.display = 'none';
    }
}
});

// 選択中の項目をハイライト表示
function highlightItem(items) {
    items.forEach((item, idx) => {
    // 選択中の項目に背景色を設定
    if (idx === currentIndex) {
        item.style.backgroundColor = '#cde';
        item.scrollIntoView({ block: 'nearest' });
    // それ以外は背景色をリセット 
    } else {
        item.style.backgroundColor = '';
    }
  });
}
// フォーム送信時に隠し入力欄に値を設定
document.getElementById('mainForm').addEventListener('submit', () => {
    hiddenInput.value = input.value;
});

// ページ読み込み時にメッセージから路線名を抽出して入力欄に設定
window.addEventListener('load', () => {
    const messageDiv = document.querySelector('.message');
    // メッセージから路線名を抽出する
    if (messageDiv) {
    const match = messageDiv.textContent.match(/「(.*?)」/);
    // 抽出に成功した場合、入力欄に設定
    if (match && match[1]) {
        input.value = match[1];
    }
    }
});

// ハンバーガーメニューの動作
$(function() {
  $('.hamburger').click(function() {
    $('.menu').toggleClass('open');
    $(this).toggleClass('active');
  });
});
