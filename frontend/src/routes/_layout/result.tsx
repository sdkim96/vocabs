import { Box, Button, Container, Flex, Text, VStack } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { DefaultService } from "../../client"; // 경로를 프로젝트에 맞게 수정

export const Route = createFileRoute("/_layout/result")({
  component: PaginatedResultAnalysis,
});

const ITEMS_PER_PAGE = 1; // 한 페이지당 문제지 수

function PaginatedResultAnalysis() {
  const [resultData, setResultData] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);
  const [currentPage, setCurrentPage] = useState<number>(1);

  useEffect(() => {
    // 분석 결과 API 호출
    DefaultService.analyzeMeApiResultMeGet()
      .then((response) => {
        setResultData(response.papers || []); // 문제지 데이터 저장
      })
      .catch((err) => {
        console.error(err);
        setError("분석 데이터를 가져오는 데 실패했습니다.");
      });
  }, []);

  const handleNextPage = () => {
    setCurrentPage((prev) => prev + 1);
  };

  const handlePrevPage = () => {
    setCurrentPage((prev) => Math.max(prev - 1, 1));
  };

  const paginatedData = resultData.slice(
    (currentPage - 1) * ITEMS_PER_PAGE,
    currentPage * ITEMS_PER_PAGE
  );

  return (
    <Container maxW="full">
      <Flex direction="column" align="center" pt={12}>
        {error ? (
          <Text color="red.500" fontSize="lg">
            {error}
          </Text>
        ) : (
          <VStack spacing={6} w="100%" maxW="800px">
            <Text fontSize="2xl" fontWeight="bold">
              문제지 분석 결과
            </Text>
            {paginatedData.map((paper: any, paperIndex: number) => (
              <Box key={paperIndex} p={4} bg="gray.100" borderRadius="md" w="100%">
                {paper.problems.map((problem: any, problemIndex: number) => {
                  const isCorrect = problem.candidates.some(
                    (candidate: any) => candidate.answer && candidate.checked
                  );

                  return (
                    <Box key={problemIndex} mb={4}>
                      <Text fontWeight="bold">
                        문제 {problemIndex + 1}:{" "}
                        {problem.question_type === "korean" ? "한국어" : "영어"}
                      </Text>
                      <Text>난이도: {problem.difficulty}</Text>
                      <Text color={isCorrect ? "green.500" : "red.500"}>
                        {isCorrect ? "정답" : "오답"}
                      </Text>
                      <Text mt={2}>
                        {problem.candidates.map((candidate: any, candidateIndex: number) => (
                          <Text key={candidateIndex}>
                            {candidateIndex + 1}. {candidate.text.name}{" "}
                            {candidate.checked ? "(사용자 선택)" : ""}{" "}
                            {candidate.answer ? "(정답)" : ""}
                          </Text>
                        ))}
                      </Text>
                    </Box>
                  );
                })}
              </Box>
            ))}
            <Flex justifyContent="space-between" w="100%" maxW="800px">
              <Button
                colorScheme="blue"
                onClick={handlePrevPage}
                disabled={currentPage === 1}
              >
                이전 페이지
              </Button>
              <Button
                colorScheme="blue"
                onClick={handleNextPage}
                disabled={currentPage * ITEMS_PER_PAGE >= resultData.length}
              >
                다음 페이지
              </Button>
            </Flex>
          </VStack>
        )}
      </Flex>
    </Container>
  );
}