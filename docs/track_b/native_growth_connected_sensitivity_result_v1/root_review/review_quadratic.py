"""Small exact proof check on pinned saved coefficients, no target import."""
from metadata import *
from fractions import Fraction

E=B/'ri122-native-caller-source-jgehvvxx'
p=E/'witness-01/stdout.log'
expected=dict(bytes=233035,sha256='0bb05cd98706ff6b5a8284a14019899ab1b92e76e18591a3c94ea4632e88855d')
verify(p,expected);raw=p.read_bytes()
if pin(raw)!=expected:raise ValueError('saved body changed')
v=json.loads(raw)
def rational(text):
    if not isinstance(text,str) or len(text)>20000:raise ValueError('rational text bound')
    x=Fraction(text)
    canonical=str(x.numerator) if x.denominator==1 else str(x.numerator)+'/'+str(x.denominator)
    if text!=canonical or max(abs(x.numerator).bit_length(),x.denominator.bit_length())>32768:raise ValueError('noncanonical or oversized rational')
    return x
def encode(x):return str(x.numerator) if x.denominator==1 else str(x.numerator)+'/'+str(x.denominator)
g=[rational(x)for x in v['common_gcd']['gcd_monic']]
R=rational(v['scale_domain']['R'])
if len(g)!=3 or g[2]!=1 or not 0<R<1:raise ValueError('quadratic/domain prerequisites')
at_one=sum(g,Fraction(0));derivative_at_one=g[1]+2
if not at_one>0 or not derivative_at_one<0:raise ValueError('simple positivity proof not applicable')
records=[]
if [r['record']for r in v['Q2_contrasts']]!=list(range(1,16)):raise ValueError('contrast domain')
for row in v['Q2_contrasts']:
    q=[rational(x)for x in row['Q2_padded']]
    if len(q)!=3 or q!=[q[2]*x for x in g]:raise ValueError('not exact quadratic multiple')
    records.append(dict(record=row['record'],factor=encode(q[2]),identically_zero=q[2]==0))
nonzero=[r['record']for r in records if not r['identically_zero']]
if not nonzero:raise ValueError('no nonzero Q2')
if [r['record']for r in v['V_contrasts']]!=list(range(1,8)):raise ValueError('V domain')
deltas=[dict(record=row['record'],delta=encode(rational(row['delta_V'])))for row in v['V_contrasts']]
nonzero_v=[r['record']for r in deltas if rational(r['delta'])!=0]
if not nonzero_v:raise ValueError('no V contrast')
verify(p,expected)
print(save('ROOT_QUADRATIC_POSITIVITY_REVIEW.json',dict(schema='ri122-root-saved-quadratic-positivity-review-v1',status='EXACT_SHORT_PROOF_CHECK_PASSES_PENDING_FULL_CERTIFICATE_AUDIT',saved_certificate=ref(p),gcd=g and [encode(x)for x in g],outer_bound=encode(R),g_at_one=encode(at_one),g_derivative_at_one=encode(derivative_at_one),all_fifteen_Q2_multiples=records,seven_V_deltas=deltas,nonzero_Q2_records=nonzero,nonzero_V_records=nonzero_v,proof=['Write g(x)=g0+g1*x+x^2. Since g1+2<0, g is strictly decreasing on [0,1].','Because g(1)>0 and 0<R<1, g(x)>=g(1)>0 on (0,R]. Thus g has no root there.','Every one of the fifteen saved Q2 polynomials is its explicitly recorded scalar multiple of g, and at least one scalar is nonzero. Therefore they cannot all vanish at any admissible actual rho.','At least one of all seven saved V contrasts is nonzero. The accepted RI117/RI120 positive-prefactor identities then force both connected profiles to be nonconstant.','The accepted necessary constancy alternative excludes the unchanged 28-child positive repair at epsilon=1/4, conditional on the full saved coefficient/input audit and the stated native model premises.'],scope='All saved contrast polynomials and a short independent positivity proof only. Does not reconstruct the forty held rows, fixture execution or custody; these require separate accepted evidence.',full_saved_arithmetic_audit_complete=False,new_native_probability_rows=0,actual_scale_evaluated=False,physical_result=False,programme_complete=False)))
