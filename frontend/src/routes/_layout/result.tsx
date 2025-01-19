import { Container, Flex, Grid, GridItem, Text, VStack } from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { ResultsService } from "../../client"; // 경로는 프로젝트에 맞게 수정
import TestDetail from "../../components/Test/TestDetail"; // 경로는 프로젝트에 맞게 수정

export const Route = createFileRoute("/_layout/result")({
  component: ResultAnalysis,
});

function ResultAnalysis() {
  const [metaData, setMetaData] = useState<any[]>([]);
  const [selectedPaper, setSelectedPaper] = useState<any | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    ResultsService.getMyResultOnlyMetaApiV1ResultsMetaMeGet()
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
    ResultsService.getMyResultOfPaperApiV1ResultsSpecificMeGet({ paperId, testId })
      .then((response) => {
        setSelectedPaper(response.paper || null);
      })
      .catch((err) => {
        console.error(err);
        setError("시험지 상세 정보를 가져오는 데 실패했습니다.");
      });
  };

  return (
    <Container maxW="full" py={8}>
      <Flex direction="column" align="center">
        {error ? (
          <Text color="red.500" fontSize="lg">
            {error}
          </Text>
        ) : selectedPaper ? (
          <TestDetail paper={selectedPaper} onBack={() => setSelectedPaper(null)} />
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