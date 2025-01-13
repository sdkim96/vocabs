import { Box, Button, Container, Flex, Radio, RadioGroup, Stack, Text } from "@chakra-ui/react";
import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { DefaultService } from "../../client"; // 경로를 프로젝트에 맞게 수정

export const Route = createFileRoute("/_layout/paper")({
  component: PaperManagement,
});

function PaperManagement() {
  const [paperData, setPaperData] = useState<any>(null);
  const [selectedAnswers, setSelectedAnswers] = useState<{ [key: string]: string }>({});
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    // 문제지 조회 API 호출
    DefaultService.getPaperApiPaperGet()
      .then((response) => {
        setPaperData(response.paper); // 문제지 데이터 저장
      })
      .catch((err) => {
        console.error(err);
        setError("문제지 데이터를 불러오는 데 실패했습니다.");
      });
  }, []);

  const handleAnswerChange = (questionId: string, answer: string) => {
    setSelectedAnswers((prev) => ({ ...prev, [questionId]: answer }));
  };

  const submitAnswers = () => {
    if (!paperData) return;

    const updatedQaSet = paperData.q_a_set.map((qa: any) => ({
      ...qa,
      answers: qa.answers.map((answer: any) => ({
        ...answer,
        checked: answer.content === selectedAnswers[qa.question.u_id] || false,
      })),
    }));

    const submitData = {
      requestBody: {
        paper_id: paperData.paper_id,
        test_id: paperData.test_id,
        binded: paperData.binded,
        q_a_set: updatedQaSet,
      },
    };

    // 문제 제출 API 호출
    DefaultService.submitPaperApiSubmitPost(submitData)
      .then((response) => {
        // 제출 성공 시 점수와 함께 /submit 페이지로 이동
        navigate({
          to: "/submit",
          search: { score: response.score.toString() }, // 점수를 쿼리 파라미터로 전달
        });
      })
      .catch((err) => {
        console.error(err);
        setError("문제를 제출하는 데 실패했습니다.");
      });
  };

  return (
    <Container maxW="full">
      <Flex direction="column" align="center" pt={12}>
        {error ? (
          <Text color="red.500" fontSize="lg">
            {error}
          </Text>
        ) : paperData ? (
          <Stack spacing={6} w="100%" maxW="800px">
            <Text fontSize="2xl" fontWeight="bold">
              문제지 조회 및 제출
            </Text>
            {paperData.q_a_set.map((qa: any) => (
              <Box key={qa.question.u_id} p={4} bg="gray.100" borderRadius="md">
                <Text mb={4} fontWeight="bold">
                  {qa.question.content}
                </Text>
                <RadioGroup
                  onChange={(value) => handleAnswerChange(qa.question.u_id, value)}
                  value={selectedAnswers[qa.question.u_id] || ""}
                >
                  <Stack spacing={3}>
                    {qa.answers.map((answer: any, index: number) => (
                      <Radio key={index} value={answer.content}>
                        {answer.content}
                      </Radio>
                    ))}
                  </Stack>
                </RadioGroup>
              </Box>
            ))}
            <Button colorScheme="teal" size="lg" onClick={submitAnswers}>
              문제 제출
            </Button>
          </Stack>
        ) : (
          <Text>문제지 데이터를 불러오는 중...</Text>
        )}
      </Flex>
    </Container>
  );
}