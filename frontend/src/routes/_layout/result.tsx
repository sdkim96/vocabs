import { Box, Button, Container, Flex, Grid, GridItem, Text, VStack } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { DefaultService } from "../../client"; // 경로는 프로젝트에 맞게 수정

export const Route = createFileRoute("/_layout/result")({
  component: ResultAnalysis,
});

function ResultAnalysis() {
  const [metaData, setMetaData] = useState<any[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    DefaultService.getMyResultOnlyMetaApiResultMetaMeGet()
      .then((response) => {
        const sortedMetaData = (response.papers || []).sort(
          (a: any, b: any) => new Date(b.created_at).getTime() - new Date(a.created_at).getTime()
        );
        setMetaData(sortedMetaData);
      })
      .catch((err) => {
        console.error(err);
        setError("메타 데이터를 가져오는 데 실패했습니다.");
      });
  }, []);

  const fetchPaperDetails = (paperId: string, testId: string) => {
    DefaultService.getResultOfPaerApiResultSpecificGet({ paperId, testId })
      .then((response) => {
        setSelectedPaper(response.paper || null);
      })
      .catch((err) => {
        console.error(err);
        setError("시험지 상세 정보를 가져오는 데 실패했습니다.");
      });
  };

  const calculateScore = (problems: any[]) => {
    const total = problems.length;
    const correct = problems.filter((problem) =>
      problem.candidates.some((candidate: any) => candidate.answer && candidate.checked)
    ).length;
    return `${correct} / ${total}`;
  };

  return (
    <Container maxW="full" py={8}>
      <Flex direction="column" align="center">
        {error ? (
          <Text color="red.500" fontSize="lg">
            {error}
          </Text>
        ) : selectedPaper ? (
          <Box w="100%" maxW="800px" p={6} bg="white" shadow="md" borderRadius="md">
            <Flex justify="space-between" align="center" mb={6}>
              <Text fontSize="2xl" fontWeight="bold">
                시험지 상세 정보
              </Text>
              <Button colorScheme="blue" onClick={() => setSelectedPaper(null)}>
                뒤로가기
              </Button>
            </Flex>
            <Text fontSize="lg" mb={6} fontWeight="bold" color="blue.500">
              점수: {calculateScore(selectedPaper.problems)}
            </Text>
            {selectedPaper.problems.map((problem: any, index: number) => {
              const isCorrect = problem.candidates.some(
                (candidate: any) => candidate.answer && candidate.checked
              );

              const correctAnswer = problem.candidates.find(
                (candidate: any) => candidate.answer
              )?.text?.k_description;

              return (
                <Box
                  key={index}
                  mb={6}
                  p={4}
                  bg="gray.50"
                  borderRadius="md"
                  display="flex"
                  flexDirection="column"
                >
                  <Flex justify="space-between" align="center">
                    <Text fontWeight="bold" fontSize="lg">
                      문제 {index + 1}
                    </Text>
                    <Flex direction="column" textAlign="right" fontSize="sm">
                      <Text>난이도: {problem.difficulty}</Text>
                      <Text>유형: {problem.question_type === "korean" ? "한국어" : "영어"}</Text>
                    </Flex>
                  </Flex>
                  <Text mt={4} fontWeight="bold" color="gray.700">
                    문제: {correctAnswer || "정답 정보 없음"}
                  </Text>
                  <Text
                    mt={2}
                    fontWeight="bold"
                    color={isCorrect ? "green.500" : "red.500"}
                  >
                    {isCorrect ? "정답" : "오답"}
                  </Text>
                  <Text mt={4} fontWeight="bold">
                    선택지:
                  </Text>
                  {problem.candidates.map((candidate: any, i: number) => (
                    <Flex
                      key={i}
                      justify="space-between"
                      align="center"
                      p={2}
                      mt={2}
                      bg={candidate.checked ? "blue.50" : "gray.100"}
                      borderRadius="md"
                    >
                      <Text>{candidate.text.name}</Text>
                      <Text color={candidate.answer ? "green.500" : "red.500"}>
                        {candidate.answer ? "정답" : ""}
                        {candidate.checked ? " (선택됨)" : ""}
                      </Text>
                    </Flex>
                  ))}
                </Box>
              );
            })}
          </Box>
        ) : (
          <VStack spacing={6} w="100%" maxW="800px">
            <Text fontSize="2xl" fontWeight="bold">
              시험지 목록
            </Text>
            <Grid templateColumns="repeat(3, 1fr)" gap={6} w="100%">
              {metaData.map((paper: any, index: number) => (
                <GridItem
                  key={paper.paper_id}
                  p={6}
                  bg="gray.100"
                  borderRadius="md"
                  textAlign="center"
                  shadow="sm"
                  cursor="pointer"
                  onClick={() => fetchPaperDetails(paper.paper_id, paper.test_id)}
                  _hover={{ bg: "blue.50", transform: "scale(1.05)" }}
                  transition="all 0.2s"
                >
                  <Text fontWeight="bold" fontSize="lg">
                    문제지 {index + 1}
                  </Text>
                  <Text fontSize="sm" color="gray.600">
                    생성일: {new Date(paper.created_at).toLocaleDateString()}
                  </Text>
                </GridItem>
              ))}
            </Grid>
          </VStack>
        )}
      </Flex>
    </Container>
  );
}