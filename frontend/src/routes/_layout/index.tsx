import { Box, Container, Text } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { UsersService } from "../../client";

export const Route = createFileRoute("/_layout/")({
  component: Dashboard,
});

function Dashboard() {
  const [user, setUser] = useState<{ id?: string; name?: string; user_type?: string } | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    // 현재 사용자 정보 가져오기
    UsersService.getMeApiV1UsersMeGet()
      .then((response) => {
        setUser(response); // 응답은 UserDTO와 일치
      })
      .catch((err) => {
        console.error(err);
        setError("사용자 정보를 불러오는 데 실패했습니다.");
      });
  }, []);

  const getUserTypeLabel = (userType?: string) => {
    switch (userType) {
      case "student":
        return "학생";
      case "teacher":
        return "선생님";
      case "admin":
        return "관리자";
      case "guest":
        return "게스트";
      default:
        return "알 수 없는 사용자 유형";
    }
  };

  return (
    <Container maxW="full">
      <Box pt={12} m={4}>
        {error ? (
          <Text color="red.500" fontSize="lg">
            {error}
          </Text>
        ) : user ? (
          <>
            <Text fontSize="2xl">
              안녕하세요, {user.name || user.id}님 👋🏼
            </Text>
            <Text fontSize="lg">
              현재 사용자 유형: {getUserTypeLabel(user.user_type)}
            </Text>
            <Text>프로젝트에 오신 것을 환영합니다! 오늘도 즐거운 학습 되세요.</Text>
          </>
        ) : (
          <Text>사용자 정보를 불러오는 중...</Text>
        )}
      </Box>
    </Container>
  );
}