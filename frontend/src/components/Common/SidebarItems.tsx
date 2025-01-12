import { Box, Flex, Icon, Text } from "@chakra-ui/react";
import { Link } from "@tanstack/react-router";

const items = [
  { title: "Dashboard", path: "/dashboard" },
  { title: "Home", path: "/home" },
  {  title: "Profile", path: "/profile" },
];

const SidebarItems: React.FC<{ onClose?: () => void }> = ({ onClose }) => {
  const textColor = "black"; // 텍스트 색상
  const bgActive = "gray.200"; // 활성 상태 배경색

  const listItems = items.map(({ title, path }) => (
    <Flex
      as={Link}
      to={path}
      w="100%"
      p={2}
      key={title}
      activeProps={{
        style: {
          background: bgActive,
          borderRadius: "12px",
        },
      }}
      color={textColor}
      onClick={onClose}
    >
    
      <Text ml={2}>{title}</Text>
    </Flex>
  ));

  return <Box>{listItems}</Box>;
};

export default SidebarItems;