import {
  Box,
  Drawer,
  DrawerBody,
  DrawerCloseButton,
  DrawerContent,
  DrawerOverlay,
  Flex,
  IconButton,
  Image,
  Text,
  useDisclosure,
} from "@chakra-ui/react";
import { FiMenu, FiLogOut } from "react-icons/fi";
import SidebarItems from "./SidebarItems";
import useAuth from "../../hooks/useAuth";
import Logo from "/assets/images/fastapi-logo.svg";

const Sidebar: React.FC = () => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const { currentUser, logout } = useAuth();
  const bgColor = "gray.100"; // 기본 배경색
  const secBgColor = "white"; // 내부 배경색
  const textColor = "black"; // 텍스트 색상

  return (
    <>
      {/* Mobile */}
      <IconButton
        onClick={onOpen}
        display={{ base: "flex", md: "none" }}
        aria-label="Open Menu"
        position="absolute"
        fontSize="20px"
        m={4}
        icon={<FiMenu />}
      />
      <Drawer isOpen={isOpen} placement="left" onClose={onClose}>
        <DrawerOverlay />
        <DrawerContent maxW="250px">
          <DrawerCloseButton />
          <DrawerBody py={8}>
            <Flex flexDir="column" justify="space-between">
              <Box>
                <Image src={Logo} alt="logo" p={6} />
                <SidebarItems onClose={onClose} />
                <Flex
                  as="button"
                  onClick={logout}
                  p={2}
                  color="red.500"
                  fontWeight="bold"
                  alignItems="center"
                >
                  <FiLogOut />
                  <Text ml={2}>Log out</Text>
                </Flex>
              </Box>
              {currentUser?.name && (
                <Text color={textColor} noOfLines={2} fontSize="sm" p={2}>
                  {currentUser?.name} 님, 안녕하세요!
                </Text>
              )}
            </Flex>
          </DrawerBody>
        </DrawerContent>
      </Drawer>

      {/* Desktop */}
      <Box
        bg={bgColor}
        p={3}
        h="100vh"
        position="sticky"
        top="0"
        display={{ base: "none", md: "flex" }}
      >
        <Flex
          flexDir="column"
          justify="space-between"
          bg={secBgColor}
          p={4}
          borderRadius={12}
        >
          <Box>
            <Image src={Logo} alt="Logo" w="180px" maxW="2xs" p={6} />
            <SidebarItems />
          </Box>
          {currentUser?.name && (
            <Text
              color={textColor} 
              noOfLines={2}
              fontSize="sm"
              p={2}
              maxW="180px"
            >
              {currentUser?.name}  님, 안녕하세요!
            </Text>
          )}
        </Flex>
      </Box>
    </>
  );
};

export default Sidebar;