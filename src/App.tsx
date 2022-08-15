import Layout from "components/Layout";
import { ResourceContextProvider } from "contexts/ResourceContext";
import { QueryClient, QueryClientProvider } from "react-query";

const queryClient = new QueryClient();

function App() {
  return (
    <div className="App">
      <QueryClientProvider client={queryClient}>
        <ResourceContextProvider>
          <Layout />
        </ResourceContextProvider>
      </QueryClientProvider>
    </div>
  );
}

export default App;
