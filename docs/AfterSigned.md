---
layout: page
title: "AfterSigned իրադարձություն"
---

# AfterSigned փաստաթղթի համակարգային իրադարձություն

AfterSigned իրադարձությունը առաջանում է տպվող տեսքի ձևավորման ժամանակ ստորագրվող PDF ձևավորելուց և էլեկտորնային ստորագրությունը դնելուց հետո։

## Շարահյուսություն

``` vb
Public Sub AfterSigned(ByVal args As EventArgsDocAfterSigned)
    ' statements
End Sub
```

Բաղադրիչներն են՝

|Պարամետր|Նկարագրություն|
|--|--|
|`oEventArgsDocAfterSigned`| EventArgsDocAfterSigned դասի օբյեկտ, որը պարունակում է տվյալներ իրադարձությունը առաջացնող փաստաթղթի և տպվող ձևանմուշի մասին։ |
