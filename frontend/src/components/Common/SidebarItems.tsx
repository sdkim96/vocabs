import { Box, Flex, Text } from "@chakra-ui/react";
import { Link } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { UsersService } from "../../client"; // 경로는 프로젝트에 맞게 수정

const SidebarItems: React.FC<{ onClose?: () => void }> = ({ onClose }) => {
  const [userType, setUserType] = useState<string | null>(null);

  useEffect(() => {
    // 사용자 정보 가져오기
    const fetchUserInfo = async () => {
      try {
        const response = await UsersService.getMeApiV1UsersMeGet();
        if (response.user_type !== undefined) {
          setUserType(response.user_type); // UserDTO의 user_type 저장
        }
      } catch (error) {
        console.error("사용자 정보를 가져오는 데 실패했습니다:", error);
      }
    };

    fetchUserInfo();
  }, []);

  const items = [
    { title: "내 정보", path: "/" }, // /api/user/me
    { title: "분석 결과", path: "/result" }, // /api/analysis
    { title: "문제 생성", path: "/paper" }, // 문제 조회와 제출
  ];

  // 관리자일 경우에만 추가
  if (userType === "admin") {
    items.push({ title: "관리자 패널", path: "/admin" });
  }

  const textColor = "black"; // 텍스트 색상
  const bgActive = "gray.200"; // 활성 상태 배경색

  return (
    <Box>
      {items.map(({ title, path }) => (
        <Flex
          as={Link}
          to={path}
          w="100%"
          p={2}
          key={title}
          _hover={{
            background: "gray.100",
            borderRadius: "12px",
          }}
          _active={{
            background: bgActive,
            borderRadius: "12px",
          }}
          color={textColor}
          onClick={onClose}
        >
          <Text ml={2}>{title}</Text>
        </Flex>
      ))}
    </Box>
  );
};

export default SidebarItems;