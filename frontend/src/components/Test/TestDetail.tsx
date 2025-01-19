import React from "react";
import { Box, Button, Flex, Text } from "@chakra-ui/react";

interface TestDetailProps {
  paper: any; // 실제 데이터 타입에 맞게 수정하세요
  onBack: () => void;
}

const calculateScore = (problems: any[]) => {
    const total = problems.length;
    const correct = problems.filter((problem) =>
      problem.candidates.some((candidate: any) => candidate.answer && candidate.checked)
    ).length;
    return `${correct} / ${total}`;
  };

const TestDetail: React.FC<TestDetailProps> = ({ paper, onBack }) => {
  return (
    <Box w="100%" maxW="800px" p={6} bg="white" shadow="md" borderRadius="md">
      <Flex justify="space-between" align="center" mb={6}>
        <Text fontSize="2xl" fontWeight="bold">
          시험지 상세 정보
        </Text>
        <Button colorScheme="blue" onClick={onBack}>
          뒤로가기
        </Button>
      </Flex>
      <Text fontSize="lg" mb={6} fontWeight="bold" color="blue.500">
        점수: {calculateScore(paper.problems)}
      </Text>
      {paper.problems.map((problem: any, index: number) => {
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
            <Text mt={2} fontWeight="bold" color={isCorrect ? "green.500" : "red.500"}>
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
  );
};

export default TestDetail;