import React, { useEffect, useState } from 'react';
import { createFileRoute } from '@tanstack/react-router';
import { DefaultService } from '../client';
import type {
  GetPaperApiPaperGetResponse,
  SubmitPaperApiSubmitPostData,
  User,
} from '../client/types.gen';
import {
  Box,
  Button,
  Flex,
  Heading,
  Spinner,
  Stack,
  Text,
  useToast,
} from '@chakra-ui/react';

export const Route = createFileRoute('/home')({
  component: Home,
});

function Home() {
  const [questions, setQuestions] = useState<GetPaperApiPaperGetResponse['paper']['q_a_set']>([]);
  const [paperID, setPaperID] = useState<string | undefined>(undefined);
  const [bindedUser, setBindedUser] = useState<User | null>(null);
  const [score, setScore] = useState<number | null>(null); // 점수 상태 추가
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const toast = useToast();

  const fetchQuestions = async () => {
    setLoading(true);
    setError(null);
    try {
      const response = await DefaultService.getPaperApiPaperGet();
      setQuestions(response.paper.q_a_set || []);
      setBindedUser(response.paper.binded || null);
      setPaperID(response.paper.id ?? undefined);
    } catch (err) {
      setError('문제를 불러오는 데 실패했습니다.');
    } finally {
      setLoading(false);
    }
  };

  const handleAnswerChange = (questionIndex: number, answerIndex: number) => {
    setQuestions((prevQuestions) =>
      prevQuestions.map((question, qIndex) => {
        if (qIndex === questionIndex) {
          return {
            ...question,
            answers: question.answers.map((answer, aIndex) => ({
              ...answer,
              checked: aIndex === answerIndex, // 선택된 답변만 checked로 설정
            })),
          };
        }
        return question;
      })
    );
  };

  const submitAnswers = async () => {
    if (!bindedUser) {
      toast({
        title: '제출 실패',
        description: '사용자 정보가 없습니다.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
      return;
    }

    const requestBody: SubmitPaperApiSubmitPostData['requestBody'] = {
      id: paperID,
      binded: bindedUser,
      q_a_set: questions,
    };

    try {
      const response = await DefaultService.submitPaperApiSubmitPost({ requestBody });
      const receivedScore = response?.score || 0; // 점수 응답 처리
      setScore(receivedScore);
      toast({
        title: '제출 성공',
        description: `문제가 성공적으로 제출되었습니다. 점수: ${receivedScore}`,
        status: 'success',
        duration: 5000,
        isClosable: true,
      });
    } catch (err) {
      toast({
        title: '제출 실패',
        description: '문제를 제출하는 데 실패했습니다.',
        status: 'error',
        duration: 5000,
        isClosable: true,
      });
    }
  };

  useEffect(() => {
    fetchQuestions();
  }, []);

  return (
    <Flex direction="column" align="center" p={5} bg="gray.50" minHeight="100vh">
      <Box width="100%" maxWidth="800px" bg="white" boxShadow="md" p={6} borderRadius="md">
        <Heading as="h1" size="lg" mb={4}>
          영어 문제 생성기
        </Heading>

        {loading ? (
          <Flex justify="center" align="center" height="200px">
            <Spinner size="lg" />
          </Flex>
        ) : error ? (
          <Text color="red.500" textAlign="center">
            {error}
          </Text>
        ) : score !== null ? ( // 점수 상태가 있으면 결과 표시
          <Box textAlign="center">
            <Heading as="h2" size="md" mb={4}>
              제출 결과
            </Heading>
            <Text fontSize="xl" fontWeight="bold" color="teal.500">
              점수: {score} / 100
            </Text>
            <Button mt={4} colorScheme="teal" onClick={fetchQuestions}>
              다시 풀기
            </Button>
          </Box>
        ) : (
          <Stack spacing={6}>
            {questions.map((q, questionIndex) => (
              <Box key={questionIndex} p={4} borderWidth="1px" borderRadius="md">
                <Text fontWeight="bold" mb={2}>
                  Q{questionIndex + 1}: {q.question.content}
                </Text>
                <Stack spacing={2}>
                  {q.answers.map((answer, answerIndex) => (
                    <label key={answerIndex}>
                      <Flex align="center">
                        <input
                          type="radio"
                          name={`q${questionIndex}`}
                          value={answer.u_id}
                          checked={answer.checked}
                          onChange={() => handleAnswerChange(questionIndex, answerIndex)}
                          style={{ marginRight: '8px' }}
                        />
                        <Text>{answer.content}</Text>
                      </Flex>
                    </label>
                  ))}
                </Stack>
              </Box>
            ))}
            <Button colorScheme="teal" size="lg" onClick={submitAnswers}>
              문제 제출
            </Button>
          </Stack>
        )}
      </Box>
    </Flex>
  );
}