import ResourcesList from "components/ResourcesList";
import { QueryClient, QueryClientProvider } from "react-query";

function App() {
  const queryClient = new QueryClient();

  return (
    <div className="App">
      <QueryClientProvider client={queryClient}>
        <ResourcesList />
      </QueryClientProvider>
    </div>
  );
}

export default App;
