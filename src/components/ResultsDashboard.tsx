import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Sun, Wind, Zap, TrendingDown, Calendar, IndianRupee } from "lucide-react";

interface RecommendationData {
  location: string;
  usage_type: string;
  system_type: string;
  recommended_size_kw: number;
  estimated_generation_kwh: number;
  monthly_savings: number;
  system_cost: number;
  payback_years: number;
  gemini_summary: string;
  details?: {
    current_consumption: number;
    remaining_consumption: number;
    current_bill: number;
    new_bill: number;
    effective_tariff: number;
    co2_reduction: number;
    slabs_used: boolean;
    subsidy_info?: {
      available: boolean;
      percentage?: number;
      amount?: number;
      gross_cost?: number;
    };
  };
}

interface ResultsDashboardProps {
  data: RecommendationData;
}

const ResultsDashboard = ({ data }: ResultsDashboardProps) => {
  const systemIcon = data.system_type === "solar" ? Sun : data.system_type === "wind" ? Wind : Zap;
  const SystemIcon = systemIcon;

  return (
    <div className="w-full max-w-6xl mx-auto space-y-6 animate-in fade-in-50 duration-500">
      {/* Summary Card */}
      <Card className="bg-gradient-to-br from-primary/5 to-accent/5 border-primary/20 shadow-[var(--shadow-elegant)]">
        <CardHeader>
          <div className="flex items-center justify-between">
            <CardTitle className="text-2xl flex items-center gap-2">
              <SystemIcon className="text-primary" />
              AI Recommendation Summary
            </CardTitle>
            <Badge className="bg-gradient-to-r from-primary to-accent text-white capitalize">
              {data.system_type}
            </Badge>
          </div>
          <CardDescription className="text-base">
            Based on analysis of {data.location}
          </CardDescription>
        </CardHeader>
        <CardContent>
          <p className="text-foreground leading-relaxed">{data.gemini_summary}</p>
        </CardContent>
      </Card>

      {/* Bill Breakdown Card */}
      {data.details && (
        <Card className="bg-gradient-to-br from-accent/5 to-primary/5 border-accent/20 shadow-[var(--shadow-elegant)]">
          <CardHeader>
            <CardTitle className="text-xl flex items-center gap-2">
              <IndianRupee className="text-accent" />
              Bill Breakdown
            </CardTitle>
            <CardDescription className="text-base">
              Detailed electricity cost analysis
            </CardDescription>
          </CardHeader>
          <CardContent>
            <div className="grid md:grid-cols-2 gap-4">
              <div>
                <h4 className="font-medium mb-2">Before {data.system_type}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Consumption:</span>
                    <span className="font-medium">{data.details.current_consumption} kWh</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Effective rate:</span>
                    <span className="font-medium">₹{data.details.effective_tariff}/unit</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Monthly bill:</span>
                    <span className="font-medium text-destructive">₹{data.details.current_bill.toLocaleString()}</span>
                  </div>
                </div>
              </div>
              
              <div>
                <h4 className="font-medium mb-2">After {data.system_type}</h4>
                <div className="space-y-2">
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Grid consumption:</span>
                    <span className="font-medium">{data.details.remaining_consumption} kWh</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">Monthly bill:</span>
                    <span className="font-medium text-emerald-600">₹{data.details.new_bill.toLocaleString()}</span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-muted-foreground">CO₂ reduction:</span>
                    <span className="font-medium text-emerald-600">{data.details.co2_reduction} tonnes/month</span>
                  </div>
                </div>
              </div>
            </div>
          </CardContent>
        </Card>
      )}
      
      {/* Metrics Grid */}
      <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Zap className="w-4 h-4" />
              System Size
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary">
              {data.recommended_size_kw} kW
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Recommended capacity
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <TrendingDown className="w-4 h-4" />
              Monthly Generation
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-accent">
              {data.estimated_generation_kwh} kWh
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Expected energy output
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <IndianRupee className="w-4 h-4" />
              Monthly Savings
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-emerald-600">
              ₹{data.monthly_savings.toLocaleString()}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Estimated bill reduction
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <IndianRupee className="w-4 h-4" />
              System Cost
            </CardTitle>
          </CardHeader>
          <CardContent>
            {data.details?.subsidy_info?.available ? (
              <>
                <p className="text-3xl font-bold text-foreground">
                  ₹{data.system_cost.toLocaleString()}
                </p>
                <div className="mt-1 space-y-1">
                  <p className="text-sm text-muted-foreground line-through">
                    ₹{data.details.subsidy_info.gross_cost?.toLocaleString()} (gross cost)
                  </p>
                  <p className="text-sm text-emerald-600">
                    -{data.details.subsidy_info.percentage}% subsidy (₹{data.details.subsidy_info.amount?.toLocaleString()})
                  </p>
                  <p className="text-xs text-muted-foreground">
                    *Under PM-KUSUM scheme for agricultural installations
                  </p>
                </div>
              </>
            ) : (
              <>
                <p className="text-3xl font-bold text-foreground">
                  ₹{data.system_cost.toLocaleString()}
                </p>
                <p className="text-sm text-muted-foreground mt-1">
                  Total installation cost
                </p>
              </>
            )}
          </CardContent>
        </Card>

        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground flex items-center gap-2">
              <Calendar className="w-4 h-4" />
              Payback Period
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-primary">
              {data.payback_years} years
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Return on investment
            </p>
          </CardContent>
        </Card>

        <Card className="hover:shadow-[var(--shadow-glow)] transition-shadow">
          <CardHeader className="pb-3">
            <CardTitle className="text-sm font-medium text-muted-foreground">
              Usage Type
            </CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-3xl font-bold text-foreground capitalize">
              {data.usage_type}
            </p>
            <p className="text-sm text-muted-foreground mt-1">
              Installation category
            </p>
          </CardContent>
        </Card>
      </div>
    </div>
  );
};

export default ResultsDashboard;
