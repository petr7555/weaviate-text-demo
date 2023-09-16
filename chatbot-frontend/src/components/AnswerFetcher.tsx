import { useEffect } from 'react';
import axios from 'axios';

type AskResponse = {
  answer: string;
};

const getAnswer = async (question: string): Promise<string> => {
  try {
    const response = await axios.post<AskResponse>('/ask', {
      question,
    });
    return response.data.answer;
  } catch (error) {
    return 'Error';
  }
};

type Props = {
  previousStep: { message: string };
  triggerNextStep: ({ value }: { value: string }) => void;
};

const AnswerFetcher = ({ previousStep, triggerNextStep }: Props) => {
  useEffect(() => {
    getAnswer(previousStep.message).then(answer => {
      triggerNextStep({ value: answer });
    });
  }, []);

  return <div>...</div>;
};

export default AnswerFetcher;
