import {
  Box,
  Button,
  Container,
  Flex,
  Spinner,
  Table,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  Text,
  VStack,
  useToast,
} from "@chakra-ui/react";
import { createFileRoute } from "@tanstack/react-router";
import { useEffect, useState } from "react";
import { DefaultService, PaperMeta, UserDTO } from "../../client"; // 경로는 프로젝트에 맞게 수정

export const Route = createFileRoute("/_layout/admin")({
  component: AdminPage,
});

function AdminPage() {
  const toast = useToast();
  const [students, setStudents] = useState<UserDTO[]>([]);
  const [metaData, setMetaData] = useState<PaperMeta[]>([]);
  const [selectedStudent, setSelectedStudent] = useState<UserDTO | null>(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchStudents();
  }, []);

  const fetchStudents = async () => {
    try {
      const response = await DefaultService.getStudentsApiStudentsGet();
      setStudents(response.students || []);
    } catch (error) {
      console.error("학생 정보를 가져오는 데 실패했습니다:", error);
      toast({
        title: "오류",
        description: "학생 정보를 가져오는 데 실패했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const fetchMetaData = async (studentId: string) => {
    setLoading(true);
    try {
      const response = await DefaultService.getStudentResultOnlyMetaApiResultMetaGet({
        studentId,
      });
      setMetaData(response.papers || []);
      setSelectedStudent(students.find((student) => student.id === studentId) || null);
    } catch (error) {
      console.error("시험 메타 데이터를 가져오는 데 실패했습니다:", error);
      toast({
        title: "오류",
        description: "시험 메타 데이터를 가져오는 데 실패했습니다.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxW="full" py={8}>
      <Flex direction="column" align="center">
        {selectedStudent ? (
          <Box w="100%" maxW="800px" p={6} bg="white" shadow="md" borderRadius="md">
            <Flex justify="space-between" align="center" mb={6}>
              <Text fontSize="2xl" fontWeight="bold">
                {selectedStudent.user_name}의 시험 목록
              </Text>
              <Button colorScheme="blue" onClick={() => setSelectedStudent(null)}>
                뒤로가기
              </Button>
            </Flex>
            {loading ? (
              <Flex justify="center" align="center" py={4}>
                <Spinner />
              </Flex>
            ) : metaData.length > 0 ? (
              <Table variant="simple">
                <Thead>
                  <Tr>
                    <Th>시험지 ID</Th>
                    <Th>테스트 ID</Th>
                    <Th>생성일</Th>
                  </Tr>
                </Thead>
                <Tbody>
                  {metaData.map((meta) => (
                    <Tr key={meta.paper_id}>
                      <Td>{meta.paper_id}</Td>
                      <Td>{meta.test_id}</Td>
                      <Td>{new Date(meta.created_at).toLocaleDateString()}</Td>
                    </Tr>
                  ))}
                </Tbody>
              </Table>
            ) : (
              <Text>시험 데이터가 없습니다.</Text>
            )}
          </Box>
        ) : (
          <VStack spacing={6} w="100%" maxW="800px">
            <Text fontSize="2xl" fontWeight="bold">
              학생 목록
            </Text>
            <Table variant="simple" size="md">
              <Thead>
                <Tr>
                  <Th>이름</Th>
                  <Th>닉네임</Th>
                  <Th>유형</Th>
                  <Th>액션</Th>
                </Tr>
              </Thead>
              <Tbody>
                {students.map((student) => (
                  <Tr key={student.id}>
                    <Td>{student.user_name}</Td>
                    <Td>{student.user_nickname || "없음"}</Td>
                    <Td>{student.user_type}</Td>
                    <Td>
                      <Button
                        size="sm"
                        colorScheme="blue"
                        onClick={() => fetchMetaData(student.id!)}
                      >
                        시험 목록 보기
                      </Button>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </VStack>
        )}
      </Flex>
    </Container>
  );
}

export default AdminPage;