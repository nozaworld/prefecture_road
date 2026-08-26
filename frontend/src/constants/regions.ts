import type { Region } from '../types';

// 7地方区分。ヘッダーの都道府県選択と複数県横断検索の一覧をグループ化するために使う。
export const REGIONS: Region[] = [
  {
    name: '北海道・東北',
    codes: ['hokkaido', 'aomori', 'iwate', 'miyagi', 'akita', 'yamagata', 'fukushima'],
  },
  { name: '関東', codes: ['ibaraki', 'tochigi', 'gunma', 'saitama', 'chiba', 'tokyo', 'kanagawa'] },
  {
    name: '中部',
    codes: ['niigata', 'toyama', 'ishikawa', 'fukui', 'yamanashi', 'nagano', 'gifu', 'shizuoka', 'aichi'],
  },
  { name: '近畿', codes: ['mie', 'shiga', 'kyoto', 'osaka', 'hyogo', 'nara', 'wakayama'] },
  { name: '中国', codes: ['tottori', 'shimane', 'okayama', 'hiroshima', 'yamaguchi'] },
  { name: '四国', codes: ['tokushima', 'kagawa', 'ehime', 'kochi'] },
  {
    name: '九州・沖縄',
    codes: ['fukuoka', 'saga', 'nagasaki', 'kumamoto', 'oita', 'miyazaki', 'kagoshima', 'okinawa'],
  },
];
