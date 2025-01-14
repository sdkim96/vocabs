import { Box, Flex, Text, VStack } from "@chakra-ui/react";
import { Link } from "@tanstack/react-router";


const SidebarItems: React.FC<{ onClose?: () => void }> = ({ onClose }) => {
  const items = [
    { title: "내 정보", path: "/" }, // /api/user/me
    { title: "분석 결과", path: "/result" }, // /api/analysis
    { title: "문제 생성", path: "/paper" }, // 문제 조회와 제출
  ];

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