import React from "react";
import { ViewIcon, ViewOffIcon } from "@chakra-ui/icons";
import {
  Button,
  Container,
  FormControl,
  FormErrorMessage,
  Icon,
  Image,
  Input,
  InputGroup,
  InputRightElement,
  Link,
  Text,
  useBoolean,
} from "@chakra-ui/react";
import {
  Link as RouterLink,
  createFileRoute,
  redirect,
} from "@tanstack/react-router";
import { type SubmitHandler, useForm } from "react-hook-form";

import Logo from "/assets/images/fastapi-logo.svg";
import { UsersService } from "../client"; // API 서비스 클래스
import { isLoggedIn } from "../hooks/useAuth";

export const Route = createFileRoute("/login")({
  component: Login,
  beforeLoad: async () => {
    if (isLoggedIn()) {
      throw redirect({
        to: "/", // 로그인된 사용자는 대시보드로 리다이렉트
      });
    }
  },
});

type LoginFormInputs = {
  username: string;
  password: string;
};

function Login() {
  const [show, setShow] = useBoolean(); // 비밀번호 표시 토글 상태
  const { register, handleSubmit, formState } = useForm<LoginFormInputs>({
    mode: "onBlur",
    defaultValues: {
      username: "",
      password: "",
    },
  });

  const { errors, isSubmitting } = formState; // 폼 상태 추출
  const [error, setError] = React.useState<string | null>(null); // 오류 메시지 상태

  const onSubmit: SubmitHandler<LoginFormInputs> = async (data) => {
    if (isSubmitting) return;

    setError(null); // 이전 오류 초기화

    try {
      const response = await UsersService.signInApiV1UsersSignInPost({
        formData: {
          username: data.username,
          password: data.password,
          grant_type: "password",
          scope: "",
        },
      });

      if (response.access_token) {
        localStorage.setItem("token", response.access_token); // 토큰 저장
        window.location.href = "/"; // 대시보드로 리다이렉트
      }
    } catch (err) {
      console.error("로그인 실패:", err);
      setError("아이디 또는 비밀번호가 잘못되었습니다."); // 오류 메시지 설정
    }
  };

  return (
    <Container
      as="form"
      onSubmit={handleSubmit(onSubmit)}
      h="100vh"
      maxW="sm"
      alignItems="stretch"
      justifyContent="center"
      gap={4}
      centerContent
    >
      <Image
        src={Logo}
        alt="FastAPI logo"
        height="auto"
        maxW="2xs"
        alignSelf="center"
        mb={4}
      />
      <FormControl id="username" isInvalid={!!errors.username || !!error}>
        <Input
          id="username"
          {...register("username", {
            required: "아이디를 입력하세요.",
          })}
          placeholder="아이디"
          type="text"
          required
        />
        {errors.username && (
          <FormErrorMessage>{errors.username.message}</FormErrorMessage>
        )}
      </FormControl>
      <FormControl id="password" isInvalid={!!error}>
        <InputGroup>
          <Input
            {...register("password", {
              required: "비밀번호를 입력하세요.",
            })}
            type={show ? "text" : "password"}
            placeholder="비밀번호"
            required
          />
          <InputRightElement
            color="ui.dim"
            _hover={{
              cursor: "pointer",
            }}
          >
            <Icon
              as={show ? ViewOffIcon : ViewIcon}
              onClick={setShow.toggle}
              aria-label={show ? "비밀번호 숨기기" : "비밀번호 보기"}
            />
          </InputRightElement>
        </InputGroup>
        {error && <FormErrorMessage>{error}</FormErrorMessage>}
      </FormControl>
      <Link as={RouterLink} to="/recover-password" color="blue.500">
        비밀번호를 잊으셨나요?
      </Link>
      <Button variant="primary" type="submit" isLoading={isSubmitting}>
        로그인
      </Button>
      <Text>
        계정이 없으신가요?{" "}
        <Link as={RouterLink} to="/signup" color="blue.500">
          회원가입
        </Link>
      </Text>
    </Container>
  );
}

export default Login;