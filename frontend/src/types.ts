// APIとフロントエンドで共有するデータ形状の定義

export interface Road {
  id: number;
  prefecture: string;
  prefecture_display?: string;
  section_number: number;
  route_name: string;
  start_point: string;
  end_point: string;
  municipality_code: string;
  expressway_type: string;
  section_length: number;
  upstream_point: string;
  upstream_traffic: number;
  downstream_point: string;
  downstream_traffic: number;
  total_traffic: number;
  day_night_ratio: number;
  congestion_degree: number;
  upstream_speed: number;
  downstream_speed: number;
  road_width: number;
  speed_limit: number;
  // ROAD_FIELDSの内容に応じてroad[f.name]のように動的にアクセスするため，
  // 上記に定義していないキーへのアクセスも許容する
  [key: string]: string | number | undefined;
}

// フォーム入力中はすべてinputのvalue（文字列）で保持する
export type RoadFormData = {
  section_number: string;
} & Record<string, string>;

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface PrefectureOption {
  code: string;
  name: string;
}

export interface Region {
  name: string;
  codes: string[];
}

export interface RoadField {
  name: string;
  label: string;
  formLabel: string;
  type: 'text' | 'number';
  required?: boolean;
}

export interface SortOption {
  value: string;
  label: string;
}

export interface Filters {
  routeName: string;
  lengthValue: string;
  lengthOp: 'gte' | 'lte';
  sortColumn: string;
  sortOrder: 'ASC' | 'DESC';
}

export interface SearchParams {
  prefecture: string;
  route_name: string;
  length_value: string;
  length_op: string;
  sort_column: string;
  sort_order: string;
  page: number;
  page_size: number;
}
