import { Box, Container, Flex, Text } from "@chakra-ui/react";
import { createFileRoute, useSearch } from "@tanstack/react-router";
import { useEffect } from "react";

export const Route = createFileRoute("/_layout/submit")({
  component: SubmitResult,
});

function SubmitResult() {
  const score = useSearch({
    from: "/_layout/submit",
    select: (search) => {
      return search.score
    },
  });

  useEffect(() => {
    console.log("Updated score:", score); // 상태 업데이트 확인
  }, [score]);

  console.log(score);

  return (
    <Container maxW="full">
      <Flex direction="column" align="center" pt={12}>
        <Box p={4} bg="gray.100" borderRadius="md">
          <Text fontSize="2xl" fontWeight="bold">
            제출 완료 🎉
          </Text>
          <Text mt={4} fontSize="lg">
            당신의 점수는 <strong>{score}</strong> 점입니다.
          </Text>
        </Box>
      </Flex>
    </Container>
  );
}