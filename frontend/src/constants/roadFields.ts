import type { RoadField, SortOption } from '../types';

export const ROAD_FIELDS: RoadField[] = [
  { name: 'route_name', label: '路線名', formLabel: '路線名', type: 'text', required: true },
  { name: 'start_point', label: '起点側路線名', formLabel: '起点側', type: 'text' },
  { name: 'end_point', label: '終点側路線名', formLabel: '終点側', type: 'text' },
  { name: 'municipality_code', label: '市区町村コード', formLabel: '市区町村コード', type: 'text' },
  { name: 'expressway_type', label: '専用道路', formLabel: '自動車専用道路の別', type: 'text' },
  { name: 'section_length', label: '区間延長(km)', formLabel: '区間延長', type: 'number' },
  { name: 'upstream_point', label: '上り観測地点', formLabel: '上り地点地名', type: 'text' },
  { name: 'upstream_traffic', label: '24h上り交通量(台)', formLabel: '上り交通量', type: 'number' },
  { name: 'downstream_point', label: '下り観測地点', formLabel: '下り地点地名', type: 'text' },
  { name: 'downstream_traffic', label: '24h下り交通量(台)', formLabel: '下り交通量', type: 'number' },
  { name: 'total_traffic', label: '24h交通量合計(台)', formLabel: '交通量合計', type: 'number' },
  { name: 'day_night_ratio', label: '昼夜率', formLabel: '昼夜率', type: 'number' },
  { name: 'congestion_degree', label: '混雑度', formLabel: '混雑度', type: 'number' },
  { name: 'upstream_speed', label: '上り速度(km/h)', formLabel: '上り旅行速度', type: 'number' },
  { name: 'downstream_speed', label: '下り速度(km/h)', formLabel: '下り旅行速度', type: 'number' },
  { name: 'road_width', label: '幅員(m)', formLabel: '道路部幅員', type: 'number' },
  { name: 'speed_limit', label: '最高速度(km/h)', formLabel: '指定最高速度', type: 'number' },
];

export const SORT_OPTIONS: SortOption[] = ROAD_FIELDS.map((f) => ({ value: f.name, label: f.label }));
