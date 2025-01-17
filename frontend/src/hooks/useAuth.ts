import { useState, useEffect } from "react";
import { UsersService, UserDTO } from "../client";

export const isLoggedIn = (): boolean => {
  const token = localStorage.getItem("token");
  return !!token;
};

type AuthState = {
  currentUser: UserDTO | null;
  isLoading: boolean;
  error: string | null;
};

const useAuth = () => {
  const [state, setState] = useState<AuthState>({
    currentUser: null,
    isLoading: true,
    error: null,
  });

  useEffect(() => {
    const fetchUser = async () => {
      if (!isLoggedIn()) {
        setState({ currentUser: null, isLoading: false, error: null });
        return;
      }

      try {
        const response = await UsersService.getMeApiV1UsersMeGet(); // 유저 정보 가져오기
        setState({
          currentUser: response ?? null, // 바인딩된 사용자 정보
          isLoading: false,
          error: null,
        });
      } catch (err) {
        console.error("Failed to fetch user:", err);
        setState({ currentUser: null, isLoading: false, error: "Failed to fetch user data." });
      }
    };

    fetchUser();
  }, []);

  const logout = () => {
    localStorage.removeItem("token"); // 토큰 제거
    window.location.href = "/login"; // 로그인 화면으로 리다이렉트
  };

  return {
    ...state,
    logout,
  };
};

export default useAuth;