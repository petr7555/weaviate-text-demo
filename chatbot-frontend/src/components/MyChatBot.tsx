import ChatBot from 'react-simple-chatbot';
import AnswerFetcher from './AnswerFetcher';

const MyChatBot = () => {
  return (
    <ChatBot
      headerTitle="Q&A"
      botDelay={0}
      userDelay={0}
      steps={[
        {
          id: '1',
          message: 'What is your question?',
          trigger: '2',
          replace: true,
        },
        {
          id: '2',
          user: true,
          trigger: '3',
        },
        {
          id: '3',
          trigger: '4',
          // eslint-disable-next-line @typescript-eslint/ban-ts-comment
          // @ts-ignore
          component: <AnswerFetcher />,
          waitAction: true,
          asMessage: true,
          replace: true,
        },
        {
          id: '4',
          trigger: '2',
          message: ({ previousValue }: { previousValue: string }) => previousValue,
        },
      ]}
    />
  );
};

export default MyChatBot;
