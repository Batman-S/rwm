import axios, { AxiosInstance } from "axios";
import { API_BASE_URL } from "../../config/config";

export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});
