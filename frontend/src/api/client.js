import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

const client = axios.create({
  baseURL: API_BASE_URL,
});

export const getPrefectures = () => client.get('/prefectures/').then((res) => res.data);

export const getRouteNames = (prefecture) =>
  client.get('/roads/route_names/', { params: { prefecture } }).then((res) => res.data);

export const searchRoads = (params) =>
  client.get('/roads/', { params }).then((res) => res.data);

export const createRoad = (data) => client.post('/roads/', data).then((res) => res.data);

export const updateRoad = (id, data) =>
  client.patch(`/roads/${id}/`, data).then((res) => res.data);

export const bulkDeleteRoads = (ids) =>
  client.post('/roads/bulk_delete/', { ids }).then((res) => res.data);

export default client;
