import {
    Box,
    Button,
    Container,
    FormControl,
    FormLabel,
    Input,
    Text,
    VStack,
    useToast,
  } from "@chakra-ui/react";
  import { createFileRoute, useNavigate } from "@tanstack/react-router";
  import { useState } from "react";
  import { DefaultService } from "../client"; // 경로는 프로젝트에 맞게 수정
  
  export const Route = createFileRoute("/signup")({
    component: SignUp,
  });
  
  function SignUp() {
    const toast = useToast();
    const navigate = useNavigate();
  
    // State for form fields
    const [name, setName] = useState(""); // 아이디
    const [password, setPassword] = useState("");
    const [userName, setUserName] = useState(""); // 유저의 실제 이름
    const [userNickname, setUserNickname] = useState("");
  
    const [isSubmitting, setIsSubmitting] = useState(false);
  
    // Form submission handler
    const handleSignUp = async () => {
      if (!name || !password || !userName) {
        toast({
          title: "입력 오류",
          description: "필수 입력 필드를 모두 채워주세요.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
        return;
      }
  
      setIsSubmitting(true);
  
      try {
        await DefaultService.signUpApiSignUpPost({
          requestBody: {
            name, // 아이디
            password,
            user_name: userName, // 유저의 실제 이름
            user_nickname: userNickname,
          },
        });
  
        toast({
          title: "회원가입 성공",
          description: "회원가입이 완료되었습니다. 로그인 페이지로 이동합니다.",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
  
        // Clear the form
        setName("");
        setPassword("");
        setUserName("");
        setUserNickname("");

        navigate({
          to: "/login", // 로그인된 사용자는 대시보드로 리다이렉트
        });
  
      } catch (error) {
        console.error("회원가입 오류:", error);
        toast({
          title: "회원가입 실패",
          description: "오류가 발생했습니다. 다시 시도해주세요.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      } finally {
        setIsSubmitting(false);
        
      }
    };
  
    return (
      <Container maxW="md" py={8}>
        <Box bg="white" shadow="md" p={6} borderRadius="md">
          <Text fontSize="2xl" fontWeight="bold" mb={6}>
            회원가입
          </Text>
          <VStack spacing={4}>
            <FormControl isRequired>
              <FormLabel>아이디</FormLabel>
              <Input
                placeholder="아이디를 입력하세요"
                value={name}
                onChange={(e) => setName(e.target.value)}
              />
            </FormControl>
            <FormControl isRequired>
              <FormLabel>이름</FormLabel>
              <Input
                placeholder="이름을 입력하세요"
                value={userName}
                onChange={(e) => setUserName(e.target.value)}
              />
            </FormControl>
            <FormControl>
              <FormLabel>닉네임</FormLabel>
              <Input
                placeholder="닉네임을 입력하세요"
                value={userNickname}
                onChange={(e) => setUserNickname(e.target.value)}
              />
            </FormControl>
            <FormControl isRequired>
              <FormLabel>비밀번호</FormLabel>
              <Input
                type="password"
                placeholder="비밀번호를 입력하세요"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
              />
            </FormControl>
            <Button
              colorScheme="blue"
              onClick={handleSignUp}
              isLoading={isSubmitting}
            >
              회원가입
            </Button>
          </VStack>
        </Box>
      </Container>
    );
  }