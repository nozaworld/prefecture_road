import axios from 'axios';
import type { PaginatedResponse, PrefectureOption, Road, SearchParams } from '../types';

const API_BASE_URL = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
  // Django側のセッションCookie・CSRFトークンをクロスオリジンでも送受信する
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

export const getPrefectures = (): Promise<PrefectureOption[]> =>
  client.get('/prefectures/').then((res) => res.data);

export const getRouteNames = (prefecture: string): Promise<string[]> =>
  client.get('/roads/route_names/', { params: { prefecture } }).then((res) => res.data);

export const searchRoads = (params: SearchParams): Promise<PaginatedResponse<Road>> =>
  client.get('/roads/', { params }).then((res) => res.data);

export const createRoad = (data: Record<string, unknown>): Promise<Road> =>
  client.post('/roads/', data).then((res) => res.data);

export const updateRoad = (id: number, data: Record<string, unknown>): Promise<Road> =>
  client.patch(`/roads/${id}/`, data).then((res) => res.data);

export const bulkDeleteRoads = (ids: number[]): Promise<{ deleted: number }> =>
  client.post('/roads/bulk_delete/', { ids }).then((res) => res.data);

export default client;
